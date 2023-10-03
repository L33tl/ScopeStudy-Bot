from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

request_location_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(
        text='Отправить геолокацию',
        request_location=True
    )]
], resize_keyboard=True,
    one_time_keyboard=True
)


def main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(
            text='Сегодня',
        )],
        [KeyboardButton(
            text='Завтра'
        )],
        # [KeyboardButton(
        #     text='Выбрать день'
        # )],
    ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Воспользуйтесь меню ↓'
    )
