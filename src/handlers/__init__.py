from aiogram import Dispatcher, types

from handlers.followers import start_cmd, refollow_cmd
from handlers.admin import admin_login_cmd, cancel_handler_login, process_password
from handlers.sender import sendall_cmd, cancel_handler_sender, process_text
from handlers.sender import skip_photo, process_photo, handle_albums
from handlers.buttons import markups_mapping
from states import formAdmin, formSend

def setup(dp: Dispatcher):
    # register followers
    dp.register_message_handler(start_cmd, commands='start')
    dp.register_message_handler(refollow_cmd, commands='refollow')

    # register admin
    dp.register_message_handler(admin_login_cmd, commands=['admin'])
    dp.register_message_handler(cancel_handler_login, state=formAdmin.password, commands=['cancel'])
    dp.register_message_handler(process_password, state=formAdmin.password)

    # register sender
    dp.register_message_handler(sendall_cmd, commands=['sender'])
    dp.register_message_handler(cancel_handler_sender, state='*', commands=['cancel'])
    dp.register_message_handler(process_text, state=formSend.text)
    dp.register_message_handler(skip_photo, state=formSend.photo, commands=['skip'])
    dp.register_message_handler(handle_albums, is_media_group=True, state=formSend.photo,
                                content_types=types.ContentType.ANY)
    dp.register_message_handler(process_photo, state=formSend.photo, content_types='photo')


    # register buttons
    dp.register_message_handler(markups_mapping)
