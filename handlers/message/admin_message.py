from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database.db import Database

from config import admin_id, group_id
from bot import bot
from handlers.state.admin_mailing_list import AdminMessage
from markups import adminMenu, delKeyboard

db = Database('database/database.db')


async def admin_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           f"Добро пожаловать, Администратор!", parse_mode="Markdown", reply_markup=adminMenu)

async def admin_menu(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, f"Ваше меню:", reply_markup=adminMenu)
    else:
        await bot.send_message(message.from_user.id, "Ошибка\nВы не администратор!")


async def admin_choice(message: types.Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    async with state.proxy() as data:
        data['admin_choice'] = message.text
    if message.text == 'Бан':
        await bot.send_message(message.from_user.id,
                               "Введите ID пользователя, которого Вы хотите забанить:")
        await AdminMessage.user_message.set()
    elif message.text == 'Разбан':
        await bot.send_message(message.from_user.id,
                               "Введите ID пользователя, которого Вы хотите разбанить:")
        await AdminMessage.user_message.set()
    elif message.text == 'Кол-во юзеров':
        await bot.send_message(message.from_user.id, f"Количество пользователей: {db.get_count_users()}",
                               reply_markup=adminMenu)
    elif message.text == 'Рассылка':
        await bot.send_message(message.from_user.id,
                               "Укажите сообщение, которое будет отправлено всем пользователям:")
        await AdminMessage.user_message.set()
    else:
        await bot.send_message(message.from_user.id,
                               "Такой команды нет!", reply_markup=delKeyboard)
        await admin_start(message)


async def admin_msg_to_user(message: types.Message):
    admin_cmd, user_id, text = None, None, None
    try:
        admin_cmd, user_id, text = message.text.split(" ", 2)
    except:
        await bot.send_message(message.chat.id, f"Вы допустили ошибку в написании сообщения, пример:\n"
                                                f"/tell 1234567 Test")
    if db.user_exists(user_id):
        try:
            await bot.send_message(user_id, f"*Administratordan xabar!*\n\n{text}", parse_mode="Markdown")
            await bot.send_message(message.chat.id, f"Сообщение успешно отправлено!")
        except:
            await bot.send_message(message.chat.id, f"Пользователь заблокировал бота!")
    else:
        await bot.send_message(message.chat.id, f"Данный пользователь не запускал бота!")


async def get_admin_doc(message: types.Message):
    if message.photo:
        document_id = message.photo[0].file_id
    else:
        document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    await bot.send_message(message.from_user.id, f'file_id: {file_info.file_id}')


def setup(dp: Dispatcher):
    dp.register_message_handler(admin_start,
                                lambda msg: msg.from_user.id == admin_id,
                                commands=['start'],
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(admin_menu,
                                lambda msg: msg.from_user.id == admin_id,
                                commands=['menu'],
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(admin_msg_to_user,
                                lambda msg: msg.chat.id == group_id or msg.chat.id == admin_id,
                                commands=['tell'])
    dp.register_message_handler(admin_choice,
                                lambda msg: msg.from_user.id == admin_id,
                                content_types=['text'],
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(get_admin_doc,
                                lambda msg: msg.from_user.id == admin_id,
                                content_types=['photo', 'document'],
                                chat_type=[types.ChatType.PRIVATE])
