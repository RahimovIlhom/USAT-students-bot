from data.config import REDIS_URL
from loader import router
from .throttling import ThrottlingMiddleware
from .check_subs_func import check_subs

redis_url = REDIS_URL

# Routerga middleware qo‘shish
router.message.middleware(ThrottlingMiddleware(redis_url))
