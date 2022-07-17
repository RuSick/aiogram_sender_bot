from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from data.db import Database

bot = Bot(config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(config.DATABASE)