from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("IP")  # Xosting ip manzili

DB_NAME = env.str("POSTGRES_DB")
DB_USER = env.str("POSTGRES_USER")
DB_PASSWORD = env.str("POSTGRES_PASSWORD")
DB_HOST = env.str("POSTGRES_HOST")
DB_PORT = env.str("POSTGRES_PORT")

REDIS_URL = env.str("REDIS_URL")

PRIVATE_CHANNELS = env.list("PRIVATE_CHANNELS")

SEND_PHOTO_URL = env.str("SEND_PHOTO_URL")
SEND_MESSAGE_URL = env.str("SEND_MESSAGE_URL")
