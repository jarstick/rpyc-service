import aioredis

from authRpc.config.conf import REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DB

redis = None


async def initialRedis():
    global redis
    redis = await aioredis.from_url(url=f"redis://{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")


