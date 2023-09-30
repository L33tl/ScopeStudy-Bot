from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.reply import request_location_keyboard
from bot.misc.states import LocationStates


async def change_location(callback: CallbackQuery, state: FSMContext):
    await state.set_state(LocationStates.CHANGE_LOCATION)
    await callback.message.reply(
        f'Введите адрес (Обязательно напишите город, точность на ваше усмотрение) или просто отправьте свою геолокацию',
        reply_markup=request_location_keyboard)


def register_callback_handlers(dp: Dispatcher):
    dp.callback_query.register(change_location, F.data == 'change_location')
