import asyncio
from asyncio import Future
from uuid import uuid4

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage, AbstractChannel, AbstractQueue

from settings import get_settings

async def image_to_ascii_art() -> str:
    image_key = await _store_image()
    return await _process_stored_image(image_key)

async def _store_image() -> str:
    await asyncio.sleep(0.2)
    return "image key"

async def _process_stored_image(image_key: str) -> str:
    settings = get_settings()
    async with await connect(
        f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}/",
        timeout=settings.timeout_seconds) as connection:
        channel = await connection.channel()
        callback_queue = await channel.declare_queue(exclusive=True,
                                                     timeout=get_settings().timeout_seconds)
        correlation_id = str(uuid4())
        future = await _wait_for_result(callback_queue, correlation_id)
        await channel.default_exchange.publish(
            Message(
                image_key.encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key="rpc_queue",
        )
        async with asyncio.timeout(get_settings().timeout_seconds):
            return await future

async def _wait_for_result(callback_queue: AbstractQueue, correlation_id: str) -> Future[str]:
    future: Future[str] = asyncio.get_running_loop().create_future()
    async def on_response(message: AbstractIncomingMessage) -> None:
        if message.correlation_id != correlation_id:
            # TODO: logging
            return
        future.set_result(message.body.decode())

    await callback_queue.consume(on_response, no_ack=True)
    return future
