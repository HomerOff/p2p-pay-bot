import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import comment_group_id
from database.db import Database

from bot import bot
from markups import mainChoice, delKeyboard, userMenu

db = Database('database/database.db')


class UserProposalComment(StatesGroup):
    user_message = State()
    user_apply = State()


async def manager_proposal_user_message(message: types.Message, state: FSMContext):
    if not message.media_group_id:
        async with state.proxy() as data:
            data['message_text'] = 'Matn yo\'q'
            if message.text or message.caption:
                data['message_text'] = message.text or message.caption

            data['file_id'] = None
            if message.photo:
                document_id = message.photo[0].file_id
                file_info = await bot.get_file(document_id)
                data['file_id'] = file_info.file_id

            await bot.send_message(message.from_user.id, 'Bu taklif yuborilsinmi?',
                                   parse_mode="Markdown",
                                   reply_markup=mainChoice)

        await UserProposalComment.next()
    else:
        await bot.send_message(message.from_user.id, 'Xabar notoʻgʻri kiritildi (faqat bitta rasmdan foydalaning)',
                               reply_markup=delKeyboard)


async def manager_proposal_user_apply(message: types.Message, state: FSMContext):
    if message.text == '✅':
        async with state.proxy() as data:
            data['user_apply'] = message.text
        db.set_user_comment(message.from_user.id)
        try:
            if data['file_id']:
                await bot.send_photo(comment_group_id, data['file_id'],
                                     f'Комментарий пользователя: {data["message_text"]}\n'
                                     f'\nID пользователя: `{str(message.from_user.id)}`\n'
                                     f'Имя пользователя: @{message.from_user.username}\n',
                                     parse_mode="Markdown")
            else:
                await bot.send_message(comment_group_id,
                                       f'Комментарий пользователя: {data["message_text"]}\n'
                                       f'\nID пользователя: `{str(message.from_user.id)}`\n'
                                       f'Имя пользователя: @{message.from_user.username}\n',
                                       parse_mode="Markdown")
        except Exception as e:
            logging.error(e)
            await bot.send_message(message.from_user.id, 'Xabar yuborishda xatolik yuz berdi!', reply_markup=userMenu)
            await state.finish()

        await bot.send_message(message.from_user.id, 'Taklif muvaffaqiyatli yuborildi!', reply_markup=userMenu)
    else:
        await bot.send_message(message.from_user.id, 'Siz taklifni bekor qildingiz!', reply_markup=userMenu)

    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(manager_proposal_user_message,
                                content_types=['photo', 'text'],
                                state=UserProposalComment.user_message,
                                chat_type=[types.ChatType.PRIVATE])

    dp.register_message_handler(manager_proposal_user_apply,
                                content_types=['text'],
                                state=UserProposalComment.user_apply,
                                chat_type=[types.ChatType.PRIVATE])
