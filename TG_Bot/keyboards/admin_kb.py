from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

item_callback = CallbackData('del', 'item_name', 'name')

#Кнопки клавиатуры админа
button_load_schedule = KeyboardButton('⬇📝Изменить расписание')
button_load = KeyboardButton('⬇️🆕 Загрузить новости')
button_delete = KeyboardButton('❌🆕 Удалить новость')
button_cancel = KeyboardButton('⬅️❌ Отмена')
button_back = KeyboardButton('⬅️Назад')
button_event = KeyboardButton('🆕 новости')
button_sendall = KeyboardButton('📢 Рассылка')
button_schedule = KeyboardButton('📝 расписание')
button_load_exercise_standards = KeyboardButton('⬇🏃 Загрузить нормативы')
button_exercise_standards = KeyboardButton('🏃 нормативы')
button_load_place = KeyboardButton('⬇🚩 Загрузить геопозицию')
button_del_place = KeyboardButton('❌🚩 Удалить геопозицию')
button_place = KeyboardButton('🚩 места занятий')
button_start_timer = KeyboardButton('⏲✅ ️Включить отправку сообщений в группу')
button_off_timer = KeyboardButton('⏲️❌ Выключить отправку сообщений в группу')
button_plan_ex = KeyboardButton('План занятия')
button_plan_ex_all = KeyboardButton('Планы занятий')
button_plan_ex_create = KeyboardButton('Изменить план занятия')

#Клавиатура админа
button_case_admin = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(button_load).add(button_delete).add(button_event).\
add(button_sendall).add(button_schedule).add(button_load_exercise_standards).add(button_exercise_standards).\
add(button_load_place).add(button_del_place).add(button_place).add(button_start_timer).add(button_off_timer).\
add(button_load_schedule).add(button_plan_ex).add(button_plan_ex_all).add(button_plan_ex_create)

#Клавиатура админа
button_case_admin_with_but_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)