from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_event = KeyboardButton('🆕 новости')
button_schedule = KeyboardButton('📝 расписание')
button_exercise_standards = KeyboardButton('🏃 нормативы')
button_place = KeyboardButton('🚩 места занятий')
# клавиатура с кнопками event_button
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client.add(button_event).add(button_schedule).add(button_exercise_standards).add(button_place)



