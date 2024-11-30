# from aioredis import Redis
#
#
# redis_url = 'redis://localhost'
#
# redis = Redis.from_url(redis_url)
#
# await redis.set(f"user:{message.from_user.id}:name", message.from_user.full_name)
#
# user_name = await redis.get(f"user:{message.from_user.id}:name")