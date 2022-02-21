from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/О_себе')
b2 = KeyboardButton('/ПМЖ')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Другое')
b5 = KeyboardButton('Поделиться номером', request_contact=True)
b6 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client.add(b1).add(b2).add(b3).add(b4)#.row(b4, b5)

kb_client_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client_2.add(b5).add(b6)