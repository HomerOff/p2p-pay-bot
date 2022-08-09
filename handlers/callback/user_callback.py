from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from config import requisites, pdf_id
from database.db import Database

from bot import bot
from messages import MESSAGES

db = Database('database/database.db')


async def send_callback(call: CallbackQuery):
    if call.data.endswith('photo'):
        if call.message.photo:
            await bot.edit_message_caption(call.from_user.id, call.message.message_id, caption=call.message.md_text,
                                           parse_mode='MarkdownV2')
        else:
            await bot.edit_message_text(call.message.md_text, call.from_user.id, call.message.message_id,
                                        parse_mode='MarkdownV2')
        await bot.send_message(call.from_user.id, MESSAGES['sendScreen'])
    elif call.data.endswith('pay'):
        paymentChoice = ReplyKeyboardMarkup(resize_keyboard=True)
        for payment in requisites.keys():
            paymentChoice.add(KeyboardButton(payment))
        await bot.send_message(call.from_user.id, MESSAGES['paymentChoice'], reply_markup=paymentChoice)
        await bot.answer_callback_query(call.id, show_alert=False)
    elif call.data.endswith('pdf'):
        await bot.send_document(call.from_user.id, pdf_id)
        await bot.answer_callback_query(call.id, show_alert=False)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(send_callback,
                                       lambda c: c.data and c.data.startswith('send'),
                                       chat_type=[types.ChatType.PRIVATE])
