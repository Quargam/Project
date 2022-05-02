from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_event = KeyboardButton('/Мероприятие')
button_schedule = KeyboardButton('/Расписание')
button_exercise_standards = KeyboardButton('/Нормативы')
button_place = KeyboardButton('/места_занятий')
# клавиатура с кнопками event_button
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_client.add(button_event).add(button_schedule).add(button_exercise_standards).add(button_place)



