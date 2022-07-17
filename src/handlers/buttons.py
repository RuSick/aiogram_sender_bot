from aiogram import types

from handlers.sender import sendall_cmd
from handlers.followers import refollow_cmd


async def markups_mapping(message: types.Message):
    if message.chat.type == 'private':
        if message.text == f'Переподписаться':
            await refollow_cmd(message)
        if message.text == f'Разослать объявление':
            await sendall_cmd(message)
