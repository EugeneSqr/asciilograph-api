import logging
import asyncio
from asyncio import Future
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
        logging.info(f"callback queue declared: {callback_queue.name}")
        callback_awaitable = await _consume_process_image_callback_queue(callback_queue, image_key)
        logging.info(f"requesting image processing for image_key={image_key}")
        await channel.default_exchange.publish(
            Message(
                image_key.encode(),
                content_type="text/plain",
                correlation_id=image_key,
                reply_to=callback_queue.name,
            ),
            routing_key=get_settings().rabbitmq_image_processing_queue,
        )
        async with asyncio.timeout(get_settings().timeout_seconds):
            logging.info(f"awaiting result for image_key={image_key}")
            return await callback_awaitable

async def _consume_process_image_callback_queue(
    callback_queue: AbstractQueue,
    correlation_id: str,
) -> Awaitable[str]:
    future: Future[str] = asyncio.get_running_loop().create_future()
    async def on_response(message: AbstractIncomingMessage) -> None:
        if message.correlation_id != correlation_id:
            logging.info(f"got correlation_id={message.correlation_id} instead of {correlation_id} "
                         f"in the '{callback_queue.name}' queue. Skipping")
            return
        logging.info(f"got result for image_key={correlation_id}")
        future.set_result(message.body.decode())

    await callback_queue.consume(on_response, timeout=get_settings().timeout_seconds, no_ack=True)
    return future

@asynccontextmanager
async def _get_channel() -> AsyncIterator[AbstractChannel]:
    async with _connection_pool.acquire() as connection:
        yield await connection.channel()
