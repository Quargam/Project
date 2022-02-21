from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

bot = Bot(token='5107816014:AAHjZleLbRnRG-Y1tsKs4XT9yhAO4QmIbek')  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot)  # ИНИЦИАЛИЗИРУЕМ диспетчер

answ = dict()

# Кнопка ссылка
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Ссылка', url='https://www.youtube.com/')
urlButton2 = InlineKeyboardButton(text='Ссылка2', url='https://www.youtube.com/')
x = [InlineKeyboardButton(text='Ссылка3', url='https://www.youtube.com/'),
     InlineKeyboardButton(text='Ссылка4', url='https://www.youtube.com/')]
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка2', url='https://www.youtube.com/'))


@dp.message_handler(commands=['ссылки'])
async def url_command(message: types.Message):
    await message.answer('Ссылочки:', reply_markup=urlkb)


inkb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Like', callback_data='like_1'), InlineKeyboardButton(text='He Like',
                                                                                    callback_data='like_-1'))


@dp.message_handler(commands=['test'])
async def test_command(message: types.Message):
    await message.answer('Голосование', reply_markup=inkb)


@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback: types.CallbackQuery):
    result = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = result
        await callback.answer('вы проголосовали')
    else:
        await callback.answer('вы уже проголосовали',show_alert=True)
    # await callback.message.answer(text='нажата инлайн кнопка')
    # await  callback.answer('нажата инлайн кнопка',
    #                        show_alert=False)  # show_alert=True всплывает окно которое нужно подтвердить

executor.start_polling(dp, skip_updates=True)
