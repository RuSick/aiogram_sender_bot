from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from bot import db, bot
from states import formAdmin
from keyboards import replyMarkups as nav


async def admin_login_cmd(message: types.Message):
    if message.chat.type == 'private':
        if not db.get_user_flags(message.from_user.id)[0]:
            await formAdmin.password.set()
            await message.reply(f"Введите пароль или отмените ввод командой /cancel:")
        else:
            await bot.send_message(message.from_user.id,
                                   f"Вы вошли как админ!",
                                   reply_markup=nav.adminMenu)


async def cancel_handler_login(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply(f'Вход отменен.',
                        reply_markup=nav.mainMenu)


async def process_password(message: types.Message, state: FSMContext):
    """Process ur password"""
    if message.text != config.PASSWORD:
        await message.delete()
        return await bot.send_message(message.from_user.id,
                                      f"Пароль введен неверно!")
    # Finish our conversation
    await state.finish()
    db.set_admin(message.from_user.id, 1)
    await message.delete()
    await bot.send_message(message.from_user.id,
                           f"Добро пожаловать, {message.from_user.username}",
                           reply_markup=nav.adminMenu)
