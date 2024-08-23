# 配置 Redis
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = "123456"
REDIS_DB = 3

# MySQL配置
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "nameko"
MYSQL_CONNECTION_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# SERVER配置
SECRET_KEY = "HSfV1HqrMmFKvGNC"
ASCII_TEXT = r"""
                          _                               _            
                     _   | |                             (_)           
          ____ _   _| |_ | | _      ___  ____  ____ _   _ _  ____ ____ 
         / _  | | | |  _)| || \    /___)/ _  )/ ___) | | | |/ ___) _  )
        ( ( | | |_| | |__| | | |  |___ ( (/ /| |    \ V /| ( (__( (/ / 
         \_||_|\____|\___)_| |_|  (___/ \____)_|     \_/ |_|\____)____)
"""

# JWT配置
JWT_SECRET = 'AZl1OwtT7M$D5#uo'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24  # 24 hours
JWT_REFRESH_EXP_DELTA_SECONDS = 60 * 60 * 24 * 7  # 7 days
