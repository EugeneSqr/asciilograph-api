import asyncio
from asyncio import Future
from uuid import uuid4
from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable

from aio_pika import connect, Message
from aio_pika.pool import Pool
from aio_pika.abc import (
    AbstractConnection,
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
)

from settings import get_settings


async def _get_connection() -> AbstractConnection:
    settings = get_settings()
    return await connect(
        f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}/",
        timeout=settings.timeout_seconds)

_connection_pool: Pool[AbstractConnection] = Pool(
    _get_connection,
    max_size=get_settings().rabbitmq_connection_pool_size,
)

async def process_image(image_key: str) -> str:
    async with _get_channel() as channel:
        callback_queue = await channel.declare_queue(exclusive=True,
                                                     timeout=get_settings().timeout_seconds)
        correlation_id = str(uuid4())
        callback_awaitable = await _consume_process_image_callback_queue(callback_queue,
                                                                         correlation_id)
        await channel.default_exchange.publish(
            Message(
                image_key.encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key=get_settings().rabbitmq_image_processing_queue,
        )
        async with asyncio.timeout(get_settings().timeout_seconds):
            return await callback_awaitable

async def _consume_process_image_callback_queue(
    callback_queue: AbstractQueue,
    correlation_id: str,
) -> Awaitable[str]:
    future: Future[str] = asyncio.get_running_loop().create_future()
    async def on_response(message: AbstractIncomingMessage) -> None:
        # TODO: consider using message.process context manager to reject if something goes wrong
        if message.correlation_id != correlation_id:
            # TODO: logging
            return
        future.set_result(message.body.decode())

    await callback_queue.consume(on_response, timeout=get_settings().timeout_seconds)
    return future

@asynccontextmanager
async def _get_channel() -> AsyncIterator[AbstractChannel]:
    async with _connection_pool.acquire() as connection:
        yield await connection.channel()