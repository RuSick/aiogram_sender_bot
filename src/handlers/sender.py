import logging
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import bot, db
from keyboards import replyMarkups as nav
from states import formSend


# ------------Sender states-----
async def sendall_cmd(message: types.Message):
    if message.chat.type == 'private':
        if db.get_user_flags(message.from_user.id)[0]:
            await formSend.text.set()
            await message.reply(f'Заполните следующую форму: текст; фото; '
                                f'\n Если хотите отменить заполнение отправьте команду /cancel')
            await bot.send_message(message.from_user.id, f'Введите текст, который хотите разослать:')
        else:
            await message.reply(f"Доступ запрещен",
                                reply_markup=nav.mainMenu)


async def cancel_handler_sender(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply(f'Рассылка отменена.',
                        reply_markup=nav.adminMenu)


async def process_text(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data['text'] = message.text
        await formSend.next()
        await message.reply(f"Отправьте фото или команду /skip, чтобы оставить это поле пустым")
    else:
        return await message.reply(f"Отправьте текст, который вы хотите разослать ")


async def skip_photo(message: types.Message, state: FSMContext):
    users = db.get_users()
    async with state.proxy() as data:
        text = data['text']
    for row in users:
        if int(row[1]) == 1:
            try:
                await bot.send_message(row[0],
                                       text)
                logging.info("Message sended")
            except:
                db.set_active(row[0], 0)
                logging.info(row[1], 'active sets')
    await bot.send_message(message.from_user.id, "Сообщения разосланы!")
    await state.finish()


async def process_photo(message: types.Message, state: FSMContext):
    if message.photo[-1].file_id:
        photo_id = message.photo[-1].file_id
        async with state.proxy() as data:
            data['photo'] = photo_id
            users = db.get_users()
            for row in users:
                if int(row[1]) == 1:
                    try:
                        await bot.send_photo(row[0],
                                             data['photo'],
                                             caption=data['text'])
                        logging.info("Message sended")
                    except:
                        db.set_active(row[0], 0)

        await bot.send_message(message.from_user.id, "Сообщения разосланы!")
        await state.finish()
    else:
        return await message.reply(f"Отправьте ФОТО или напишите /skip, чтобыть оставить это поле пустым")


async def handle_albums(message: types.Message, album: List[types.Message], state: FSMContext):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("Этот тип не поддерживается")
    #if media group empty -> send photo
    async with state.proxy() as data:
        users = db.get_users()
        for row in users:
            if int(row[1]) == 1:
                try:
                    await bot.send_media_group(row[0],
                                               media_group)
                    await bot.send_message(row[0], data['text'])
                    logging.info("Message sended")
                except:
                    db.set_active(row[0], 0)
    await state.finish()
