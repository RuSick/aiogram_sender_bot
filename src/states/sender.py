from aiogram.dispatcher.filters.state import StatesGroup, State


class formSend(StatesGroup):
    text = State()
    photo = State()