from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from utils.db_api import Database, Messages, RedisClient

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

db = Database()
messages = Messages()
redis_client = RedisClient(redis_url=config.REDIS_URL)


# Bot ishga tushganida kerakli obyektlarni olish
async def on_startup_bot():
    await db.connect()
    await messages.load_messages()
    await redis_client.connect_redis()


async def stop_bot():
    # await bot.close()
    # await dp.storage.close()
    await db.disconnect()
    await redis_client.close()
