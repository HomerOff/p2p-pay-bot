from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.db import Database

from config import admin_id, requisites, pdf_id
from bot import bot
from handlers.state.user_photo import UserPhoto
from handlers.state.user_proposal_comment import UserProposalComment
from markups import userMenu, delKeyboard, screenshot, helpMenu, sendNumber
from messages import MESSAGES

db = Database('database/database.db')


async def user_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if db.get_status(message.from_user.id) == 'ban':
        await bot.send_message(message.from_user.id,
                               MESSAGES['ban'], reply_markup=userMenu)
    else:
        await bot.send_message(message.from_user.id, MESSAGES['user_start'],
                               parse_mode="Markdown", reply_markup=userMenu, disable_web_page_preview=True)


async def user_choice(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if message.text == MESSAGES['btnHelp']:
        await user_start(message)
    elif db.get_status(message.from_user.id) == 'ban':
        await bot.send_message(message.from_user.id,
                               MESSAGES['ban'])
    else:
        if message.text == MESSAGES['btnPay']:
            paymentChoice = ReplyKeyboardMarkup(resize_keyboard=True)
            for payment in requisites.keys():
                paymentChoice.add(KeyboardButton(payment))
            paymentChoice.add(KeyboardButton('🏠'))
            await bot.send_message(message.from_user.id, MESSAGES['paymentChoice'],
                                   reply_markup=paymentChoice)
        elif message.text == MESSAGES['btnPdf']:
            await bot.send_document(message.from_user.id, pdf_id,
                                    reply_markup=userMenu)
        elif message.text == MESSAGES['btnComment']:
            if not db.get_user_comment(message.from_user.id):
                await bot.send_message(message.from_user.id,
                                       MESSAGES['comment_message'],
                                       parse_mode='Markdown',
                                       reply_markup=delKeyboard)
                await UserProposalComment.user_message.set()
            else:
                await bot.send_message(message.from_user.id, MESSAGES['comment_exist_message'])
        elif message.text in requisites.keys():
            await bot.send_message(message.from_user.id, f"{requisites.get(message.text)}\n" + MESSAGES['requisites_message'],
                                   parse_mode="Markdown", reply_markup=screenshot)
        elif message.text == '🏠':
            await user_start(message)
        else:
            await bot.send_message(message.from_user.id,
                                   MESSAGES['unknown_message'], reply_markup=delKeyboard)
            await user_start(message)


async def get_user_photo(message: types.Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if db.get_status(message.from_user.id) == 'response':
        await bot.send_message(message.from_user.id, MESSAGES['response_message'])
    elif db.get_status(message.from_user.id)[:7] == 'success':
        await bot.send_message(message.from_user.id, MESSAGES['success_message'],
                               parse_mode="Markdown", reply_markup=helpMenu)
    elif db.get_status(message.from_user.id) == 'ban':
        await bot.send_message(message.from_user.id,
                               MESSAGES['ban'])
    elif message.photo and not message.media_group_id:
        document_id = message.photo[0].file_id
        file_info = await bot.get_file(document_id)

        async with state.proxy() as data:
            data['file_id'] = file_info.file_id

        await bot.send_message(message.from_user.id, MESSAGES['send_phone_message'],
                               reply_markup=sendNumber)
        await UserPhoto.user_num.set()


def setup(dp: Dispatcher):
    dp.register_message_handler(user_start,
                                lambda msg: not msg.from_user.id == admin_id,
                                commands=['start'],
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(user_choice,
                                lambda msg: not msg.from_user.id == admin_id,
                                content_types=['text'],
                                chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(get_user_photo,
                                lambda msg: not msg.from_user.id == admin_id,
                                content_types=['photo'],
                                chat_type=[types.ChatType.PRIVATE])
