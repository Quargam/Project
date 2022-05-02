from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_cancel = KeyboardButton('/Отмена')
button_back = KeyboardButton('/Назад')
button_event = KeyboardButton('/Мероприятие')
button_sendall = KeyboardButton('/Рассылка')
button_schedule = KeyboardButton('/Расписание')
button_load_exercise_standards = KeyboardButton('/Загрузить_нормативы')

#Клавиатура админа
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_event).\
add(button_sendall).add(button_schedule).add(button_load_exercise_standards)

#Клавиатура админа
button_case_admin_with_but_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)