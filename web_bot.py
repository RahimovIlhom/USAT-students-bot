import logging
import ssl
import sys

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import middlewares, filters, handlers
from loader import dp, on_startup_bot, stop_bot, bot
from utils import on_startup_notify
from utils.set_bot_commands import set_default_commands

from environs import Env

env = Env()
env.read_env()

WEB_SERVER_HOST = env.str('WEB_SERVER_HOST')
WEB_SERVER_PORT = env.int('WEB_SERVER_PORT')

WEBHOOK_PATH = env.str('WEBHOOK_PATH')
WEBHOOK_SECRET = env.str('WEBHOOK_SECRET')
BASE_WEBHOOK_URL = env.str('BASE_WEBHOOK_URL')

WEBHOOK_SSL_CERT = env.str('WEBHOOK_SSL_CERT')
WEBHOOK_SSL_PRIV = env.str('WEBHOOK_SSL_PRIV')


async def on_startup() -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

    # Bot ishga tushganida kerakli obyektlarni olish
    await on_startup_bot()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify()


# def main() -> None:
#     dp.startup.register(on_startup)
#     dp.shutdown.register(stop_bot)
#
#     app = web.Application()
#
#     webhook_requests_handler = SimpleRequestHandler(
#         dispatcher=dp,
#         bot=bot,
#         secret_token=WEBHOOK_SECRET,
#     )
#     webhook_requests_handler.register(app, path=WEBHOOK_PATH)
#
#     setup_application(app, dp, bot=bot)
#
#     web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(stop_bot)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, ssl_context=context)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
