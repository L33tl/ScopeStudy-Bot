import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.user import register_user_handlers
from bot.handlers.callbacks import register_callback_handlers
from settings import get_settings
from bot.misc.commands import set_commands
from utils.logger import logger


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(871333900, f'Bot Started!\n/start')
    await bot.send_message(752981093, f'Bot Started!\n/start')
    # await bot.send_message(752981093, f'Bot Started!\n/start')


async def stop_bot(bot: Bot):
    await bot.send_message(871333900, '79')


def register_all_handlers(dp: Dispatcher):
    dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    register_user_handlers(dp)
    register_callback_handlers(dp)


async def main():
    logger.info('Starting bot')

    settings = get_settings('.env')

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    register_all_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped!')
