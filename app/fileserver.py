from uuid import uuid4
from typing import AsyncIterator

import aioftp

from settings import get_settings


async def store_image(request_stream: AsyncIterator[bytes]) -> str:
    settings = get_settings()
    filename = str(uuid4())
    async with aioftp.Client.context(settings.fileserver_address,
                                     user=settings.fileserver_user,
                                     password=settings.fileserver_password) as ftp_client:
        async with ftp_client.upload_stream(filename) as upload_stream:
            async for file_chunk in request_stream:
                await upload_stream.write(file_chunk)
    return filename
