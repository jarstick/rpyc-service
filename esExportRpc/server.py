import asyncio

from loguru import logger as log
from rpyc import ThreadedServer

from authRpc.config.conf import ASCII_TEXT
from esExportRpc.service.esExportService import EsExportService


async def startServer():
    log.success(ASCII_TEXT)
    server = ThreadedServer(EsExportService, port=18861,
                            protocol_config={"sync_request_timeout": 30, "allow_public_attrs": True})
    await server.start()


if __name__ == "__main__":
    asyncio.run(startServer())
