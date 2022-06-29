import asyncio
import json
import uuid

from typing import MutableMapping
from hashlib import sha256
from prettytable import PrettyTable

from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue
)

from config import COMMAND_COUNT, BOOK_HEADERS
from exceptions import NotFoundError
from database.models.user import User
from database.user import user_system
from logger import logger


class RpcClient(object):
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self, user: User) -> None:
        self.id : uuid.UUID = user.id
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = asyncio.get_running_loop()
        self.user = user

    async def connect(self) -> "RpcClient":
        self.connection = await connect(
            url="amqp://admin:admin@localhost/",
            loop=self.loop,
        )

        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(
            exclusive=True,
            name=self.user.name
        )

        client_data = {
            'id' : self.id.hex,
            'command' : 'init_client'
        }
        
        await self.callback_queue.consume(self._on_response)
        await self.channel.default_exchange.publish(
            Message(
                correlation_id=str(uuid.uuid4()),
                content_type="application/json",
                body=json.dumps(client_data).encode(),
                reply_to=self.callback_queue
            ),
            routing_key="rpc_queue"
        )

        return self

    def _on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            print(f" [e] Что-то пошло не так... {message!r}")
            return

        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, data: str):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        published = await self.channel.default_exchange.publish(
            Message(
                correlation_id=correlation_id,
                body=data.encode(),
                content_type="application/json",
                reply_to=self.callback_queue
            ),
            routing_key="rpc_queue"
        )

        return bytes(await future).decode(), published


async def main() -> None:
    try:
        logged_in = False

        print(' [x] Нажмите ctrl+c чтобы выйти.')
        # while not logged_in:
        #     logged_in, user = try_logged_in()

        client = await RpcClient(User('admin', 'admin')).connect()
        print(f" [x] Поключился к серверу как {client.user.name}.")

        while True:
            render_user_commands()
            is_command_select = False

            while not is_command_select:
                is_command_select, command = try_select_command()

            message = {
                'id' : client.id.hex
            }

            match command:
                case 0:
                    message['command'] = 'get_all'
                case 1:
                    message['command'] = 'add'
                    message['object'] = create_book()
                case 2:
                    message['command'] = 'find_by_author'
                    message['object'] = get_book_author()
                case 3:
                    message['command'] = 'find_by_name'
                    message['object'] = get_book_name()
                case 4:
                    message['command'] = 'del'
                    message['object'] = get_book_id()
                case 5:
                    message['command'] = 'bye'
                case 6:
                    message['command'] = 'stop'
                case _:
                    logger.error(f' [x] Неверная команда: {command!r}')
                    continue

            request = json.dumps(message)
            response, published = await client.call(request)
            
            print('===', published.attributes())

            response = json.loads(response)

            match command:
                case 0:
                    render_book_list(response)
                case 1:
                    print(response['message'])
                case 2:
                    render_book_list(response)
                case 3:
                    render_book_list(response)
                case 4:
                    print(response['message'])
                case 5:
                    print(' [x] Отключение от сервера.')
                    exit(0)
                case 6:
                    print(' [x] Сервер выключается.')
                    print(' [x] Отключение от сервера.')
                    exit(0)
    except KeyboardInterrupt:
        await client.callback_queue.delete()
        exit(0)
    except Exception as e:
        logger.error(e)


def render_user_commands():
    print(" [•] Выберете команду:")
    print(" [•] 0 - Показать список книг.")
    print(" [•] 1 - Добавить книгу.")
    print(" [•] 2 - Найти книгу по автору.")
    print(" [•] 3 - Найти книгу по названию.")
    print(" [•] 4 - Удалить книгу.")
    print(" [•] 5 - Выйти.")
    print(" [•] 6 - Выключить сервер.")


def try_select_command():
    command = input(' [•] Введите номер комманды: ')

    if not command.isdigit() or not 0 <= int(command) <= COMMAND_COUNT:
        print(' [x] Неизвестная команда!')
        return False, None

    return True, int(command)


def try_logged_in():
    name = input(' [•] Введите имя пользователя: ')
    password = input(' [•] Введи пароль пользователя: ')

    try:
        user = user_system.get_by_name(name=name)
    except NotFoundError as e:
        print(' [e] Неверное имя пользователя.')
        logger.error(e)
        return False, None

    if user.password != sha256(bytes(password, 'utf-8')).hexdigest():
        print(' [e] Неверный пароль пользователя.')
        return False, None

    return True, user


def render_book_list(books: list):
    table = PrettyTable(BOOK_HEADERS)
    for book in books:
        table.add_row([
            book['id'],
            book['name'],
            book['author'],
            book['pages']
        ])
    print(table)


def create_book():
    book = {}
    book['name'] = input(" [•] Введите название книги: ")
    book['author'] = input(" [•] Введите автора: ")
    book['pages'] = input(" [•] Введите кол-во страниц: ")

    return book


def get_book_id():
    while True:
        id = input(" [•] Введите ID книги: ")

        if id.isdigit():
            return id

        print(" [e] Номер должен содержать только цифры!")


def get_book_name():
    return input(' [•] Введите название книги: ')


def get_book_author():
    return input(' [•] Введите автора книги: ')


def run():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        task = loop.create_task(main())
        task.add_done_callback(
            lambda t: print(' [x] Отключение...')
        )
    else:
        asyncio.run(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        exit(0)
