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
        [KeyboardButton(
            text='Выбрать день'
        )],
        [KeyboardButton(
            text='Показать ДЗ'
        )]
    ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Воспользуйтесь меню ↓'
    )


def registration_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(
            text='Настроить погоду',
        )],
        [KeyboardButton(
            text='Собрать своё расписание'
        )],
        [KeyboardButton(
            text='Продолжить\n(Всё можно будет изменить в настройках)'
        )]
    ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Настройте бота'
    )
