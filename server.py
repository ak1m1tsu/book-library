import asyncio
import json

from uuid import UUID

from aio_pika import Connection, Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractExchange
)

from logger import logger


class RpcServer(object):
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
        self._connection = Connection(
            "amqp://server:test@localhost/",
            loop=self._loop
        )
        await self._connection.connect()
        self._channel = await self._connection.channel()
        self._exchange = self._channel.default_exchange
        self._queue = await self._channel.declare_queue('rpc_queue')
        logger.info(f'Сервер подключился к {self._connection.url} без ошибок.')

    async def _send(self, client: dict, response: str) -> None:
        self._exchange.publish(
            Message(
                correlation_id=client['correlation_id'],
                content_type='application/json',
                body=json.dumps(response).encode()
            ),
            routing_key=client['name']
        )

    async def _get_response(self, content: str) -> str:
        data = json.loads(content)        
        response = await self._execute_command(data=data)
        return response

    async def _close(self) -> dict:
        self._connection.close()
        return { 'command': 'close' }

    async def _execute_command(self, data: dict):
        response: dict[str, str] = {}

        match data['command']:
            case 'init_client':
                pass
            case 'get_all':
                pass
            case 'add':
                pass
            case 'delete':
                pass
            case 'find_by_author':
                pass
            case 'find_by_name':
                pass
            case 'bye':
                pass
            case 'stop':
                response = await self._close()
            case _:
                logger.info(data)
        
        return json.dumps(response)

    async def _stop(self):
        await self._loop.close()
        logger.info('Сервер выключен.')

    async def run_until_complete(self) -> None:
        await self._connect()

        async with self._queue.iterator() as iterator:
            message: AbstractIncomingMessage
            async for message in iterator:
                try:
                    async with message.process(requeue=False):
                        assert message.reply_to is not None
                        content = message.body.decode()
                        
                        client = {
                            'id': content['id'],
                            'name': message.reply_to,
                            'correlation_id': message.correlation_id,
                        }

                        response = await self._get_response(content=content)
                        logger.info(f'Получен ответ для {client["name"]}: {response}')

                        await self._send(client=client,response=response)
                        logger.info(f'Ответ для {client["name"]} успешно отправлен')

                        if response['command'] == 'close':
                            await self._stop()
                except Exception as e:
                    logger.error(e)


async def main() -> None:
    await RpcServer().run_until_complete()

if __name__ == "__main__":
    asyncio.run(main())