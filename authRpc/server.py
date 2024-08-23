import asyncio

from loguru import logger as log
from rpyc import ThreadedServer

from authRpc.authService import AuthService
from authRpc.config.conf import ASCII_TEXT


async def startServer():
    log.success(ASCII_TEXT)
    server = ThreadedServer(AuthService, port=18861, protocol_config={"sync_request_timeout": 30, "allow_public_attrs": True})
    await server.start()


if __name__ == "__main__":
    asyncio.run(startServer())