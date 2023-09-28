import logging

from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext

from bot.keyboards.reply import *
from bot.keyboards.inline import *
from bot.misc.states import LocationStates


async def get_start(message: Message, state: FSMContext):
    if await state.get_state() == LocationStates.HAVE_LOCATION:
        return await message.reply('Вы уже зарегистрированны\nХотите воспользоваться /settings?')
    await state.set_state(LocationStates.UNKNOWN_LOCATION)
    await message.reply(f'Добро пожаловать, {message.from_user.first_name}!\nСначала настройте бота:',
                        reply_markup=registration_keyboard())


async def change_location(message: Message, state: FSMContext):
    await state.set_state(LocationStates.CHANGE_LOCATION)
    await message.reply('Введите адрес (точность на ваше усмотрение) или просто отправьте свою геолокацию',
                        reply_markup=request_location_keyboard)


async def set_location(message: Message, state: FSMContext):
    if message.location:
        location = message.location.longitude, message.location.latitude
    else:
        logging.info(f'By toponym - {message.text}')
        location = ...
    await state.set_state(LocationStates.HAVE_LOCATION)
    await state.set_data({'longlat': location})
    await message.reply(f'Ваше местоположение сохранено!', reply_markup=main_keyboard())
    logging.info(f'User`s {message.from_user.id} location - {location}')


async def show_today(message: Message, state: FSMContext):
    pass


async def show_tomorrow(message: Message):
    pass


async def show_chosen_day(message: Message):
    pass


async def show_settings(message: Message):
    await message.answer('Настройки', reply_markup=settings_keyboard)


def register_user_handlers(dp: Dispatcher):
    dp.message.register(get_start, CommandStart())
    dp.message.register(change_location, F.text == 'Настроить погоду')
    dp.message.register(set_location, F.location)

    dp.message.register(show_today, F.text == 'Сегодня')
    dp.message.register(show_tomorrow, F.text == 'Завтра')
    dp.message.register(show_chosen_day, F.text == 'Выбрать день')

    dp.message.register(show_settings, Command('settings'))
