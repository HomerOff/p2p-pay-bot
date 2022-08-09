from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import group_id
from database.db import Database

from bot import bot
from markups import sendNumber, userMenu, mainChoice, delKeyboard

db = Database('database/database.db')


class UserPhoto(StatesGroup):
    user_num = State()
    user_apply = State()


async def set_user_num(message: types.Message, state: FSMContext):
    if message.contact:
        async with state.proxy() as data:
            data['user_number'] = message.contact.phone_number
        await bot.send_message(message.from_user.id, 'Ushbu ekran tasvirini yuborasizmi?',
                               reply_markup=mainChoice)
        await UserPhoto.user_apply.set()
    elif message.text == '🚫':
        await bot.send_message(message.from_user.id, 'Ekran tasvirini yuborish bekor qilindi!\n'
                                                     'Tayyor bo\'lgach, skrinshotni yana yuboring!',
                               reply_markup=delKeyboard)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id,
                               'Noto\'g\'ri qiymat kiritilgan, quyidagi tugmalardan birini tanlang',
                               reply_markup=sendNumber)


async def set_user_apply(message: types.Message, state: FSMContext):
    if message.text == '✅':
        async with state.proxy() as data:
            data['user_apply'] = message.text
        btnApply = InlineKeyboardButton("✅", callback_data=f'1_{str(message.from_user.id)}')
        btnDeny = InlineKeyboardButton("🚫", callback_data=f'0_{str(message.from_user.id)}')
        keyboard_user = InlineKeyboardMarkup(resize_keyboard=True).add(btnApply, btnDeny)
        await bot.send_photo(group_id, data['file_id'], f'ID пользователя: {str(message.from_user.id)}\n'
                                                        f'Имя пользователя: @{message.from_user.username}\n'
                                                        f'Номер пользователя: {str(data["user_number"])}',
                             reply_markup=keyboard_user)
        db.set_status(message.from_user.id, 'response')
        await bot.send_message(message.from_user.id, "Rahmat!\n"
                                                     "Skrinshot tekshirish uchun yuborilgan.\n"
                                                     "\nTekshiruvdan so'ng siz ushbu botda xabar olasiz, kuting.",
                               reply_markup=userMenu)
    else:
        await bot.send_message(message.from_user.id, 'Ekran tasvirini yuborish bekor qilindi!\n'
                                                     'Tayyor bo\'lgach, skrinshotni yana yuboring!',
                               reply_markup=userMenu)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(set_user_num,
                                content_types=['contact', 'text'],
                                state=UserPhoto.user_num,
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(set_user_apply,
                                content_types=['text'],
                                state=UserPhoto.user_apply,
                                chat_type=[types.ChatType.PRIVATE])
