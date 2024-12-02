from aioredis import Redis


class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None

    async def connect_redis(self):
        if self.redis_client is None:
            self.redis_client = await Redis.from_url(self.redis_url)

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

    async def get_user_status(self, tg_id: str):
        return (await self.get(f"user:{tg_id}:status")).decode("utf-8") if await self.exists(f"user:{tg_id}:status") else None

    async def set_user_status(self, tg_id: str, status: str):
        return await self.set(f"user:{tg_id}:status", status)

    async def delete_user_status(self, tg_id: str):
        return await self.delete(f"user:{tg_id}:status")

    async def get_user_chat_lang(self, tg_id: str):
        return (await self.get(f"user:{tg_id}:chat_lang")).decode("utf-8") if await self.exists(f"user:{tg_id}:chat_lang") else None

    async def set_user_chat_lang(self, tg_id: str, lang: str):
        return await self.set(f"user:{tg_id}:chat_lang", lang)

    async def delete_get_user_chat_lang(self, tg_id: str):
        return await self.delete(f"user:{tg_id}:chat_lang")

    async def get_user_passport(self, tg_id: str):
        return (await self.get(f"user:{tg_id}:passport")).decode("utf-8") if await self.exists(f"user:{tg_id}:passport") else None

    async def set_user_passport(self, tg_id: str, passport: str):
        return await self.set(f"user:{tg_id}:passport", passport)

    async def delete_user_passport(self, tg_id: str):
        return await self.delete(f"user:{tg_id}:passport")
