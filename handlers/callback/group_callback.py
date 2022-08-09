from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from database.db import Database

from config import group_id
from bot import bot
from markups import helpMenu, screenshot
from messages import MESSAGES

db = Database('database/database.db')


async def admin_callback(call: CallbackQuery):
    if call.data[:1].isdigit():
        user_id = int(call.data[2:])
        isPayment = int(call.data[:1])
        if isPayment:
            try:
                db.set_status(user_id, 'success')
            except:
                pass
            msg_text = f'{call.message.caption}\n\n✅  Оплата совершена успешно'
            await bot.edit_message_caption(group_id, call.message.message_id,
                                           caption=msg_text)
            await bot.send_message(user_id, MESSAGES['success_payment_message'],
                                   parse_mode="Markdown", reply_markup=helpMenu)

        else:
            if not db.get_status(user_id) == 'ban':
                db.set_status(user_id, 'start')
                msg_text = f'{call.message.caption}\n\n🚫 Оплата не была произведена!'
                await bot.edit_message_caption(group_id, call.message.message_id,
                                               caption=msg_text)
                await bot.send_message(user_id, MESSAGES['unsuccessful_payment_message'],
                                       parse_mode="Markdown", reply_markup=screenshot)
            else:
                await bot.send_message(group_id,
                                       f'Пользователь с ID `{user_id}` находится в бане!\nСообщение отправлено не было!')
    else:
        pass


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(admin_callback,
                                       lambda msg: msg.message.chat.id == group_id)