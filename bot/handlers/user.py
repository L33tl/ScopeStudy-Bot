from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
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
    if data.location:
        print(data)
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
        f'Для погоды необходима геолокация\nПросто отправьте свою геолокацию или введите адрес (Обязательно напишите город, точность на ваше усмотрение)',
        reply_markup=request_location_keyboard)


async def set_location(message: Message, state: FSMContext):
    if message.location:
        logger.info(f'By telegram location - {message.location.heading}')
        location = Location(lat=message.location.latitude, lon=message.location.longitude)
    else:
        logger.info(f'By toponym - {message.text}')
        try:
            location = WeatherManager.coordinates(toponym=message.text)
        except GeocoderException as e:
            logger.info(e)
            return await message.reply(f'Ошибка получения геолокации\nПопытайтесь ещё разок')
    await state.set_state(LocationStates.HAVE_LOCATION)
    db_worker.update_user_location(message.from_user.id, location)
    await message.reply(f'Ваше местоположение сохранено!\nlat= {location.lat} lon= {location.lon}',
                        reply_markup=main_keyboard())
    logger.info(f'User`s {message.from_user.id} location - {location}')


async def show_today(message: Message, state: FSMContext):
    user = await get_user_from_database(message.from_user.id, state)
    if await state.get_state() != LocationStates.HAVE_LOCATION:
        return await message.reply(f'У меня нет вашего местоположения\nУкажите его в настройках\n/settings')

    weather = WeatherManager.get_beauty_weather_day(mode=1, location=user.location)
    await message.reply(weather)


async def show_tomorrow(message: Message, state: FSMContext):
    user = await get_user_from_database(message.from_user.id, state)
    if await state.get_state() != LocationStates.HAVE_LOCATION:
        return await message.reply(f'У меня нет вашего местоположения\nУкажите его в настройках\n/settings')

    weather = WeatherManager.get_beauty_weather_day(mode=2, location=user.location)
    await message.reply(weather)


async def show_chosen_day(message: Message):
    pass


async def show_settings(message: Message):
    await message.answer('Настройки', reply_markup=settings_keyboard)


async def echo(message: Message):
    await message.reply('Ничего не понял, но админу написал', reply_markup=main_keyboard())
    print(
        f'from ({message.from_user.first_name} {message.from_user.last_name}) {message.from_user.full_name}:{message.from_user.id} - {message.text}')


def register_user_handlers(dp: Dispatcher):
    dp.message.register(get_start, CommandStart())
    dp.message.register(show_settings, Command('settings'))

    dp.message.register(show_today, F.text == 'Сегодня')
    dp.message.register(show_tomorrow, F.text == 'Завтра')
    dp.message.register(show_chosen_day, F.text == 'Выбрать день')

    dp.message.register(set_location, StateFilter(LocationStates.CHANGE_LOCATION))

    dp.message.register(echo, F.text)
