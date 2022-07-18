import logging

from aiogram import Dispatcher, executor

import handlers
import middlewares
from bot import dp


async def startup(dispatcher: Dispatcher):
    # Setup handlers
    logging.basicConfig(level=logging.INFO)
    logging.info("Configuring handlers...")
    handlers.setup(dispatcher)
    middlewares.setup(dispatcher)
    logging.info("Start polling")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
