from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# -------Main menu-----
btn_refollow = KeyboardButton(f'Переподписаться')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_refollow)

# -------AdminMenu-----
btn_send_all = KeyboardButton(f'Разослать объявление')
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_send_all)
