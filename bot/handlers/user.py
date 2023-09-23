from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message


async def start_bot(bot: Bot):
    await bot.send_message(871333900, f'123')


async def stop_bot(bot: Bot):
    await bot.send_message(871333900, '79')


async def get_start(message: Message):
    await message.reply(f'{message.chat.id}')
    await message.reply(f'<tg-spoiler>Hello, {message.from_user.first_name}!</tg-spoiler>')


def register_user_handlers(dp: Dispatcher):
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command('start'))
