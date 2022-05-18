from aiogram import Dispatcher

from .filter import IsPrivate, IsUserAmin, IsNotUserAmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsUserAmin)
    dp.filters_factory.bind(IsNotUserAmin)