import asyncio

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
    connection: AbstractConnection
    channel: AbstractChannel
    queue: AbstractQueue
    exchange: AbstractExchange
    loop: asyncio.AbstractEventLoop

    def __init__(self):
        self.loop = asyncio.get_running_loop()

    async def _connect(self) -> None:
        self.connection = Connection(
            "amqp://server:test@localhost/",
            loop=self.loop
        )
        self.connection.connect()
        self.channel = await self.connection.channel()
        self.exchange = self.channel.default_exchange
        self.queue = await self.channel.declare_queue('rpc_queue')

    async def _get_response(content: str):
        pass

    async def run_until_complete(self):
        await self._connect()

        async with self.queue.iterator() as iterator:
            message: AbstractIncomingMessage
            async for message in iterator:
                try:
                    async with message.process(requeue=False):
                        assert message.reply_to is not None

                        content = message.body.decode()
                        self._get_response(content=content)
                except Exception as e:
                    logger.error(e)


async def main() -> None:
    print(' [x] Ожидание запросов.')
    RpcServer().run_until_complete()

if __name__ == "__main__":
    asyncio.run(main())