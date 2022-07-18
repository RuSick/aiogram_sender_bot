from aiogram import Dispatcher

from middlewares.album_middleware import AlbumMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(middleware=AlbumMiddleware())
