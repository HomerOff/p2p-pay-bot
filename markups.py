from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove

from database.db import Database
from messages import MESSAGES

db = Database('database/database.db')

# меню пользователя

btnPay = KeyboardButton(MESSAGES['btnPay'])
btnPdf = KeyboardButton(MESSAGES['btnPdf'])
btnComment = KeyboardButton(MESSAGES['btnComment'])

userMenu = ReplyKeyboardMarkup(resize_keyboard=True)
userMenu.add(btnPdf, btnComment).add(btnPay)

# меню админа
btnBan = KeyboardButton(MESSAGES['btnBan'])
btnUnBan = KeyboardButton(MESSAGES['btnUnBan'])
btnUsers = KeyboardButton(MESSAGES['btnUsers'])
btnSpam = KeyboardButton(MESSAGES['btnSpam'])

adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnBan, btnUnBan).add(btnUsers, btnSpam)

# подтверждение действий
btnDeny = KeyboardButton('🚫')
btnApply = KeyboardButton('✅')

mainChoice = ReplyKeyboardMarkup(resize_keyboard=True)
mainChoice.add(btnDeny, btnApply)

# отправить номер телефона
btnNumber = KeyboardButton(MESSAGES['btnNumber'], request_contact=True)

sendNumber = ReplyKeyboardMarkup(resize_keyboard=True)
sendNumber.add(btnNumber).add(btnDeny)

# кнопка в приветственном сообщении
sendScreen = InlineKeyboardButton(MESSAGES['sendScreen'], callback_data='send_photo')
screenshot = InlineKeyboardMarkup(resize_keyboard=True).add(sendScreen)

# помощь
btnHelp = KeyboardButton(MESSAGES['btnHelp'])

helpMenu = ReplyKeyboardMarkup(resize_keyboard=True)
helpMenu.add(btnHelp, btnPdf).add(btnComment)

# удалить клавиатуру
delKeyboard = ReplyKeyboardRemove()
