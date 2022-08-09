from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from database.db import Database

from bot import bot
from markups import adminMenu, mainChoice, delKeyboard

db = Database('database/database.db')


class AdminMessage(StatesGroup):
    user_message = State()
    user_apply = State()


async def set_admin_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['admin_choice'] == "Рассылка":
            data['user_message'] = message.md_text
        else:
            data['user_message'] = message.text
        data['file_id'] = 0
        if message.photo:
            document_id = message.photo[0].file_id
            file_info = await (bot.get_file(document_id))
            data['file_id'] = file_info.file_id
    await AdminMessage.next()
    await bot.send_message(message.from_user.id, f'Выполнить данное действие - {data["admin_choice"]}?',
                           reply_markup=mainChoice)


async def set_admin_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_apply'] = message.text
    if message.text == '✅':
        if data['admin_choice'] == 'Бан':
            if data['user_message'].isnumeric():
                db.set_status(int(data['user_message']), 'ban')
                await bot.send_message(message.from_user.id, f'Пользователь с ID {data["user_message"]} был забанен!',
                                       reply_markup=adminMenu)
            else:
                await bot.send_message(message.from_user.id, f'Введен не верный ID, вводите только цифры!',
                                       reply_markup=adminMenu)
        elif data['admin_choice'] == 'Разбан':
            if data['user_message'].isnumeric():
                db.set_status(int(data['user_message']), 'start')
                await bot.send_message(message.from_user.id, f'Пользователь с ID {data["user_message"]} был разбанен!',
                                       reply_markup=adminMenu)
            else:
                await bot.send_message(message.from_user.id, f'Введен не верный ID, вводите только цифры!',
                                       reply_markup=adminMenu)
        elif data['admin_choice'] == 'Рассылка':
            await bot.send_message(message.from_user.id, 'Сообщения отправляются, ожидайте...',
                                   reply_markup=delKeyboard)
            user_count = 0
            for user in db.get_users():
                try:
                    if data['file_id']:
                        await bot.send_photo(user[0], data['file_id'], data['user_message'],
                                             parse_mode="MarkdownV2")
                    else:
                        await bot.send_message(user[0], data['user_message'], parse_mode="MarkdownV2")
                    user_count += 1
                except Exception as e:
                    pass
            await bot.send_message(message.from_user.id, f'Сообщение было отправлено всем пользователям!\n'
                                                         f'Количество отправленных сообщений: {str(user_count)}',
                                   reply_markup=adminMenu)
    else:
        await bot.send_message(message.from_user.id, 'Действие НЕ было выполнено!', reply_markup=adminMenu)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(set_admin_choice,
                                content_types=['photo', 'text'],
                                state=AdminMessage.user_message,
                                chat_type=[types.ChatType.PRIVATE])

    dp.register_message_handler(set_admin_result,
                                content_types=['text'],
                                state=AdminMessage.user_apply,
                                chat_type=[types.ChatType.PRIVATE])
