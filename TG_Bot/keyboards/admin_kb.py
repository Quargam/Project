from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить_Мероприятие')
button_delete = KeyboardButton('/Удалить_Мероприятие')
button_cancel = KeyboardButton('/Отмена')
button_back = KeyboardButton('/Назад')
button_event = KeyboardButton('/Мероприятие')
button_sendall = KeyboardButton('/Рассылка')
button_schedule = KeyboardButton('/Расписание')
button_load_exercise_standards = KeyboardButton('/Загрузить_нормативы')
button_exercise_standards = KeyboardButton('/Нормативы')
button_load_place = KeyboardButton('/Загрузить_геопозицию')
button_del_place = KeyboardButton('/Удалить_геопозицию')
button_place = KeyboardButton('/места_занятий')
button_start_timer = KeyboardButton('/Включить_регулярную_отправку_сообщений')
button_off_timer = KeyboardButton('/Выключить_регулярную_отправку_сообщений')


#Клавиатура админа
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_event).\
add(button_sendall).add(button_schedule).add(button_load_exercise_standards).add(button_exercise_standards).\
add(button_load_place).add(button_del_place).add(button_place).add(button_start_timer).add(button_off_timer)

#Клавиатура админа
button_case_admin_with_but_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)