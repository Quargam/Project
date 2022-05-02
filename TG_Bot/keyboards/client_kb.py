from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_event = KeyboardButton('/Мероприятие')
button_schedule = KeyboardButton('/Расписание')

# клавиатура с кнопками event_button
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client.add(button_event).add(button_schedule)



