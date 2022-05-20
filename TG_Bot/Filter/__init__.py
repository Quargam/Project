from aiogram import Dispatcher

from .filter import IsPrivate, IsUserAdmin, IsNotUserAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsUserAdmin)
    dp.filters_factory.bind(IsNotUserAdmin)