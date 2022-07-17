import logging

from aiogram import types

from bot import bot, db
from keyboards import replyMarkups as nav


async def start_cmd(message: types.Message):
    if message.chat.type == 'private':
        if db.user_exists(message.from_user.id) is None:
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id,
                                   f'Вы подписались!',
                                   reply_markup=nav.mainMenu)
            logging.info('User added')
        else:
            await bot.send_message(message.from_user.id,
                                   f"Вы уже подписаны!",
                                   reply_markup=nav.mainMenu)


async def refollow_cmd(message: types.Message):
    if message.chat.type == 'private':
        if not db.get_user_flags(message.from_user.id)[1]:  # active check with db check
            db.set_active(message.from_user.id, 1)
            await message.reply(f"Вы переподписались!")
            logging.info(f"{message.from_user.id} - Refollowed")
        else:
            await bot.send_message(message.from_user.id,
                                   f"Вы уже подписаны!")