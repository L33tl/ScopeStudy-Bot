from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Поменять местоположение',
        callback_data='change_location'
    )]
])
