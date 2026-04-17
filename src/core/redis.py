import logging

import redis.asyncio as aioredis

from src.core.config import RedisSettings

logger = logging.getLogger(__name__)


class Redis:
    def __init__(self, config: RedisSettings):
        self._config = config
        self._redis: aioredis.Redis | None = None

    async def startup(self):
        self._redis = await aioredis.Redis.from_url(url=self._config.dsn.unicode_string())
        logger.info("Redis connection is started")

    async def shutdown(self):
        await self._redis.close() if self._redis else None
        logger.info("Redis connection is closed")

    @property
    def redis(self):
        return self._redis
