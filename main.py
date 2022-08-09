import asyncio
import logging

from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot import bot

from database.db import Database
from handlers.callback import group_callback, user_callback
from handlers.message import admin_message, user_message
from handlers.state import user_photo, admin_mailing_list, user_proposal_comment

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()

dp = Dispatcher(bot, storage=MemoryStorage())

db = Database('database/database.db')


if __name__ == '__main__':
    # admin_callback.setup(dp)
    group_callback.setup(dp)
    user_callback.setup(dp)

    admin_message.setup(dp)
    # group_message.setup(dp)
    user_message.setup(dp)

    user_photo.setup(dp)
    admin_mailing_list.setup(dp)
    user_proposal_comment.setup(dp)

    executor.start_polling(dp, loop=loop, skip_updates=False)
