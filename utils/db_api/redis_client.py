from aioredis import Redis


class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None

    def connect_redis(self):
        if self.redis_client is None:
            self.redis_client = Redis.from_url(self.redis_url)

    async def close(self):
        if self.redis_client is not None:
            await self.redis_client.close()

    async def set(self, key: str, value: str):
        async with self.redis_client as redis:
            await redis.set(key, value)

    async def get(self, key: str):
        async with self.redis_client as redis:
            return await redis.get(key)

    async def delete(self, key: str):
        async with self.redis_client as redis:
            return await redis.delete(key)

    async def exists(self, key: str):
        async with self.redis_client as redis:
            return await redis.exists(key)