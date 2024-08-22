import json
from datetime import datetime, timedelta

import bcrypt
import jwt
from tortoise.exceptions import DoesNotExist

from authRpc.config.conf import JWT_EXP_DELTA_SECONDS, \
    JWT_ALGORITHM, JWT_SECRET, JWT_REFRESH_EXP_DELTA_SECONDS
from authRpc.dao.sysUser import SysUserDao
from authRpc.exc.sysUser import RpcError
from authRpc.validators.sysUser import validateEmail, validatePhone, validateUsername, validatePassword


# 用户注册
def register(session, phone, name, email, password):
    """
    用户注册
    :param session: 数据库会话
    :param phone: 手机号码
    :param name: 用户名
    :param email: 邮箱
    :param password: 明文密码
    :return:
    """
    if not validateEmail(email):
        raise RpcError(error="邮箱格式错误!")
    if not validatePhone(phone):
        raise RpcError(error="手机号码格式错误!")
    if not validatePassword(password):
        raise RpcError(error="密码长度至少8位")
    if not validateUsername(name):
        raise RpcError(error="用户名格式错误!")
    hashedPassword = hashPassword(password.strip())
    userInfo = SysUserDao.createUser(session, name, phone, hashedPassword, email)
    if userInfo is None:
        raise RpcError(error="注册用户失败")

    return json.dumps(
        {"id": userInfo.id, "username": userInfo.username, "phone": userInfo.phone, "email": userInfo.email})


def hashPassword(password: str) -> bytes:
    hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashedPassword


def verifyPassword(plainPassword: str, hashedPasswordStr: str) -> bool:
    try:
        return bcrypt.checkpw(plainPassword.encode('utf-8'), hashedPasswordStr.encode('utf-8'))
    except Exception:
        return False


def login(redisCli, session, phone, password):
    """
    用户名&密码登录
    :param phone: 手机号码, 全局唯一, 登录账号;
    :param session: mysql-session
    :param redisCli: redis-client
    :param password: 明文密码
    :return:
    """
    try:
        user = SysUserDao.queryUserByPhone(session, phone)
        if user is None:
            raise RpcError(error="用户不存在")
        passPwdVerifyFlag = verifyPassword(password, user.password)
        if not passPwdVerifyFlag:
            raise RpcError(error="账号或密码错误")
        redisRefreshToken = ""
        redisAccessToken = ""
        try:
            redisRefreshToken = redisCli.get(f"refresh_token:{user.phone}")
            redisAccessToken = redisCli.get(f"access_token:{user.phone}")
        except Exception:
            ...
        if not redisRefreshToken:
            redisCli.delete(f"access_token:{user.phone}")
            redisAccessToken = createAccessToken(user.phone)
            redisRefreshToken = createRefreshToken(user.phone)
            saveAccessToken(redisCli, user.phone, redisAccessToken)
            saveRefreshToken(redisCli, user.phone, redisRefreshToken)
        else:
            if not redisAccessToken:
                redisAccessToken = createAccessToken(user.phone)
                saveAccessToken(redisCli, user.phone, redisAccessToken)
                redisCli.expire(f"refresh_token:{user.phone}", JWT_REFRESH_EXP_DELTA_SECONDS)

        return {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "access_token": redisAccessToken,
            "refresh_token": redisAccessToken
        }

    except DoesNotExist:
        raise RpcError(error="用户不存在")


def createAccessToken(phone):
    """
    创建访问令牌
    :param phone: 手机号码
    :return: token: 令牌
    """
    payload = {
        'sub': phone,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def createRefreshToken(phone):
    """
    创建刷新令牌
    :param phone: 手机号码
    :return: token: 令牌
    """
    payload = {
        'sub': phone,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def saveRefreshToken(redisCli, phone, tokenStr):
    """
    保存刷新令牌
    :param redisCli: redis client
    :param phone: 手机号码
    :param tokenStr: 令牌
    :return:
    """
    redisCli.set(f"refresh_token:{phone}", tokenStr, JWT_REFRESH_EXP_DELTA_SECONDS)


def saveAccessToken(redisCli, phone, tokenStr):
    """
    保存刷新令牌
    :param redisCli: redis client
    :param phone: 手机号码
    :param tokenStr: 令牌
    :return:
    """
    redisCli.set(f"access_token:{phone}", tokenStr, JWT_EXP_DELTA_SECONDS)


def verifyToken(token):
    """
    验证令牌
    :param token: 令牌
    :return: None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def refreshToken(redisCli, refreshTokenStr):
    """
    刷新令牌
    :param redisCli: redis client
    :param refreshTokenStr: 刷新令牌
    :return:
    """
    try:
        payload = jwt.decode(refreshTokenStr, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        phone = payload['sub']
        storedToken = redisCli.get(f"refresh_token:{phone}")
        if storedToken and storedToken.decode() == refreshTokenStr:
            newAccessToken = createAccessToken(phone)
            return {"access_token": newAccessToken}
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def logout(redisCli, refreshTokenStr):
    """
    注销令牌
    :param redisCli: redis client
    :param refreshTokenStr: 刷新令牌
    :return:
    """
    try:
        payload = jwt.decode(refreshTokenStr, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload['sub']
        redisCli.delete(f"refresh_token:{username}")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass
