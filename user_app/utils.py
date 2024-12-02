import redis

from data.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL)
