import pytest

from bot.handlers.user import (get_user_from_database, get_start, set_location, show_today, show_tomorrow,
                               show_settings, echo)

from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


# For testing change a utils/database/db_worker.py settings path in a beginning of the file

# But actually aiogram_tests is not capable with aiogram version 3.

@pytest.mark.asyncio
async def test_echo():
    request = MockedBot(MessageHandler(echo))
    calls = await request.query(message=MESSAGE.as_object(text='Hello'))
    answer_message = calls.send_messsage.fetchone()
    assert answer_message.text == "Hello"
