import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.settings import get_settings
from bot.handlers.user import register_user_handlers

logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher):
    register_user_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Starting bot')

    settings = get_settings('.env')

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    register_all_handlers(dp)

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped!')
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
