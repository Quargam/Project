from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/О_себе')
b2 = KeyboardButton('/ПМЖ')
b3 = KeyboardButton('/Мероприятие')
b4 = KeyboardButton('/Другое')
b5 = KeyboardButton('Поделиться номером', request_contact=True)
b6 = KeyboardButton('Отправить где я', request_location=True)
b7 = KeyboardButton('/назад')

# клавиатура с кнопками b1,b2,b3,b4
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client.add(b1).add(b2).add(b3).add(b4)#.row(b4, b5)

# клавиатура с кнопками b5,b6,b7
kb_client_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client_2.add(b5).add(b6).add(b7)

