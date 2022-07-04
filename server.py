import asyncio
import json
import fcntl, sys, os

from uuid import UUID

from aio_pika import Connection, Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractExchange
)

from database.book import book_system
from exceptions import AlreadyExistsError, NotFoundError
from logger import logger
from utils import AlchemyEncoder
from config import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS


class RpcServer(object):
    '''RPC сервер для обработки сообщений
    RPC клиентов, используя RabbitMQ'''
    _connection: AbstractConnection
    _channel: AbstractChannel
    _queue: AbstractQueue
    _exchange: AbstractExchange
    _loop: asyncio.AbstractEventLoop
    _clients: dict[str: UUID]

    def __init__(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._clients = {}

    async def _connect(self) -> None:
        '''Подключение к localhost'''
        self._connection = Connection(
            f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq3/",
            loop=self._loop
        )
        await self._connection.connect()
        self._channel = await self._connection.channel()
        self._exchange = self._channel.default_exchange
        self._queue = await self._channel.declare_queue('rpc_queue')
        logger.info(f'Сервер подключился к {self._connection.url} без ошибок.')

    async def _send(self, client: dict, response: str) -> None:
        '''Отправляет ответ response в очередь client'a'''
        await self._exchange.publish(
            Message(
                correlation_id=client['correlation_id'],
                content_type='application/json',
                body=json.dumps(response, cls=AlchemyEncoder).encode()
            ),
            routing_key=client['name']
        )

    async def _get_response(self, content: dict) -> dict:
        '''Возвращает ответ для клиента в соответствии
        с коммандой запроса'''
        response = await self._get_command_response(content=content)
        return response

    def _get_books(self) -> dict:
        try:
            books = book_system.get_all()
            return {
                'command' : 'render_books',
                'message' : books
            }
        except NotFoundError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : 'Список книг пуст.'
            }
    
    def _check_book(self, book: dict):
        if book['author'].isdigit():
            return "Имя автора содержит цифры!"

        if not book['pages'].isdigit():
            return "Страницы содержат запрещенные символы!"

        return None
    
    def _delete_book(self, id: int):
        try:
            book_system.delete(id)
            return {
                'command' : 'deleted',
                'message' : 'Книга успешно удалена.'
            }
        except NotFoundError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'mesage' : 'Книга не была найдена.'
            }

    def _add_book(self, book: dict) -> dict:
        try:
            error = self._check_book(book)

            if error:
                raise ValueError(error)

            book_system.create(book['name'], book['author'], book['pages'])

            return {
                'command' : 'added',
                'message' : 'Книга успешно добавлена.'
            }
        except AlreadyExistsError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : 'Эта книга уже существует.'
            }
        except ValueError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : error
            }
        except Exception as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : 'Что-то пошло не так...'
            }

    def _find_book_by_name(self, name: str) -> dict:
        try:
            books = book_system.find_by_name(name=name)
            return {
                'command' : 'render_books',
                'message' : books
            }
        except NotFoundError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : f'Совпадения по {name!r} не найдены.'
            }

    def _find_book_by_author(self, author: str) -> dict:
        try:
            books = book_system.find_by_author(author=author)
            return {
                'command' : 'render_books',
                'message' : books
            }
        except NotFoundError as e:
            logger.error(e)
            return {
                'command' : 'error',
                'message' : f'Совпадения по {author!r} не найдены.'
            }

    async def _append_client(self, client: dict):
        if not self._clients.get(client['object']):
            self._clients[client['object']] = UUID(client['id'])
            return {
                'command' : 'connected',
                'message' : 'Подключение прошло успешно.',
                'success' : True
            }
        return {
            'command' : 'disconnet',
            'message' : 'Вы уже подключены к серверу.',
            'success' : False
        }

    async def _remove_client(self, client: dict):
        if self._clients.get(client['object']):
            self._clients.pop(client['object'])
            return {
                'command' : 'disconnect',
                'message' : 'Отключение от сервера прошло успешно.'
            }
        return {
            'command' : 'error',
            'message' : 'Пользователь не найден.'
        }

    async def _get_command_response(self, content: dict):
        response: dict[str, str] = {}

        match content['command']:
            case 'init_client':
                response = await self._append_client(content)
            case 'get_all':
                response = self._get_books()
            case 'add':
                response = self._add_book(content['object'])
            case 'delete':
                response = self._delete_book(content['object'])
            case 'find_by_author':
                response = self._find_book_by_author(content['object'])
            case 'find_by_name':
                response = self._find_book_by_name(content['object'])
            case 'bye':
                response = await self._remove_client(content)
            case 'stop':
                response['command'] = 'close'
            case _:
                logger.info(content)
        
        return response

    async def run_until_complete(self) -> None:
        await self._connect()

        async with self._queue.iterator() as iterator:
            message: AbstractIncomingMessage
            async for message in iterator:
                async with message.process():
                    try:
                        incoming_content = message.body.decode()
                        content = json.loads(incoming_content)
                        client = {
                            'id': content['id'],
                            'name': message.reply_to,
                            'correlation_id': message.correlation_id
                        }

                        response = await self._get_response(content=content)
                        logger.info(f'Получен ответ для {client["name"]}: {response}')

                        await self._send(client=client, response=response)
                        logger.info(f'Ответ для {client["name"]} успешно отправлен')

                        if response['command'] == 'close':
                            logger.info('Сервер выключен.')
                            return
                    except Exception as e:
                        logger.error(e)
                        await self._send(
                            client=client, 
                            response={
                                'command' : 'error',
                                'message' : 'Что-то пошло не так...'
                            }
                        )


async def main() -> None:
    await RpcServer().run_until_complete()


if __name__ == "__main__":
    fp = open(os.path.realpath(__file__), 'r')
    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        asyncio.run(main())
    except IOError:
        print(' [x] Сервер уже запущен.')
        sys.exit(0)
    except Exception as e:
        logger.error(e)
        