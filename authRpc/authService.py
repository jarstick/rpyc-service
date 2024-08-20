import asyncio

import redis
from rpyc import Service
from rpyc.utils.server import ThreadedServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from authRpc.authServiceImpl import logout, login, verifyToken, refreshToken, register
from authRpc.config.conf import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, REDIS_PORT, REDIS_HOST, \
    REDIS_PASSWORD, REDIS_DB, ASCII_TEXT, MYSQL_PORT
from loguru import logger as log

from authRpc.entity import BaseModel


def localSession():
    engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
                           echo=True)
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def localRedis():
    localRedisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
    return localRedisClient


class AuthService(Service):
    ALIASES = ['auth-service']
    exposed_session = localSession()
    exposed_redis = localRedis()

    def register(self, phone, username, email, password):
        """
        对外暴露的注册接口
        :param username: 姓名
        :param phone: 手机号
        :param email: 邮箱
        :param password: 明文密码
        :return:
        """
        log.info(f"用户: [{username}] 正在使用密码: [{password}] 进行注册")
        userInfo = register(AuthService.exposed_session, phone, username, email, password)
        return userInfo

    def login(self, phone, password):
        """
        对外暴露的登录接口
        :param phone: 手机号码(账号)
        :param password: 明文密码
        :return:
        """
        log.info(f"用户账号: [{phone}] 正在使用密码: [{password}] 进行登录")
        return login(AuthService.exposed_redis, AuthService.exposed_session, phone, password)

    def verifyToken(self, token):
        """
        对外暴露的验证token接口
        :param token:
        :return:
        """
        return verifyToken(token)

    def refreshToken(self, refreshTokenStr):
        """
        对外暴露的刷新token接口
        :param refreshTokenStr:
        :return:
        """
        return refreshToken(refreshTokenStr)

    def logout(self, refreshTokenStr):
        """
        对外暴露的登出接口
        :param refreshTokenStr:
        :return:
        """
        logout(refreshTokenStr)


# 启动JWT认证服务
async def startServer():
    log.success(ASCII_TEXT)
    server = ThreadedServer(AuthService, port=18861, protocol_config={"sync_request_timeout": 30, "allow_public_attrs": True})
    await server.start()


if __name__ == "__main__":
    asyncio.run(startServer())
