import logging
from typing import AsyncIterator

import aioftp
from asgi_correlation_id import correlation_id

from settings import get_settings


async def store_image(request_stream: AsyncIterator[bytes]) -> str:
    settings = get_settings()
    filename = correlation_id.get() or ""
    logging.info(f"uploading file {filename} to {settings.fileserver_address} "
                 f"as {settings.fileserver_user}")
    async with aioftp.Client.context(settings.fileserver_address,
                                     user=settings.fileserver_user,
                                     password=settings.fileserver_password) as ftp_client:
        async with ftp_client.upload_stream(filename) as upload_stream:
            async for file_chunk in request_stream:
                await upload_stream.write(file_chunk)
    logging.info(f"done uploading file {filename}")
    return filename
