from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext

from bot.keyboards.reply import *
from bot.keyboards.inline import *
from bot.misc.states import LocationStates
from bot.misc.classes import TgUser, Location

from utils.database.db_worker import DBWorker
from utils.logger import logger
from utils.weather.weather_manager import WeatherManager

from utils.exceptions.geocoder_exceptions import GeocoderException

db_worker = DBWorker()


async def get_user_from_database(user_tg_id: int, state: FSMContext) -> TgUser:
    data = db_worker.get_user(user_tg_id)
    user = TgUser(user_tg_id)
    if data is None:
        db_worker.add_user(user_tg_id)
        await state.set_state(LocationStates.UNKNOWN_LOCATION)
        return user
    if data.location is not None:
        user.location = Location(*(float(el) for el in data.location.split()))
        await state.set_state(LocationStates.HAVE_LOCATION)
    return user


async def get_start(message: Message, state: FSMContext):
    user = await get_user_from_database(message.from_user.id, state)
    if user.location:
        return await message.reply(f'Вы уже зарегистрированны!\nМожет быть Вы хотите открыть\n/settings',
                                   reply_markup=main_keyboard())
    await state.set_state(LocationStates.CHANGE_LOCATION)
    await message.reply(
        f'Для погоды необходима геолокация\nВведите адрес (Обязательно напишите город, точность на ваше усмотрение) или просто отправьте свою геолокацию',
        reply_markup=request_location_keyboard)


async def set_location(message: Message, state: FSMContext):
    if message.location:
        logger.info(f'By telegram location - {message.location.heading}')
        location = message.location.longitude, message.location.latitude
    else:
        logger.info(f'By toponym - {message.text}')
        try:
            location = WeatherManager.coordinates(toponym=message.text)
        except GeocoderException as e:
            logger.info(e)
            return await message.reply(f'Ошибка получения геолокации\nПопытайтесь ещё разок')
    await state.set_state(LocationStates.HAVE_LOCATION)
    await state.set_data({'location': location})
    db_worker.update_user_location(message.from_user.id, location)
    await message.reply(f'Ваше местоположение сохранено!', reply_markup=main_keyboard())
    logger.info(f'User`s {message.from_user.id} location - {location}')


async def show_today(message: Message, state: FSMContext):
    user = await get_user_from_database(message.from_user.id, state)
    if await state.get_state() != LocationStates.HAVE_LOCATION:
        return await message.reply(f'У меня нет вашего местоположения\nУкажите его в настройках\n/settings')

    weather = WeatherManager.get_beauty_weather(mode=1, location=user.location)
    await message.reply(weather)


async def show_tomorrow(message: Message, state: FSMContext):
    user = await get_user_from_database(message.from_user.id, state)
    if await state.get_state() != LocationStates.HAVE_LOCATION:
        return await message.reply(f'У меня нет вашего местоположения\nУкажите его в настройках\n/settings')

    weather = WeatherManager.get_beauty_weather(mode=2, location=user.location)
    await message.reply(weather)


async def show_chosen_day(message: Message):
    pass


async def show_settings(message: Message):
    await message.answer('Настройки', reply_markup=settings_keyboard)


def register_user_handlers(dp: Dispatcher):
    dp.message.register(get_start, CommandStart())
    dp.message.register(set_location, StateFilter(LocationStates.CHANGE_LOCATION))

    dp.message.register(show_today, F.text == 'Сегодня')
    dp.message.register(show_tomorrow, F.text == 'Завтра')
    dp.message.register(show_chosen_day, F.text == 'Выбрать день')

    dp.message.register(show_settings, Command('settings'))
