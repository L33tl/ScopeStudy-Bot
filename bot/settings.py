from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    load_dotenv(path)

    return Settings(
        bots=Bots(
            bot_token=getenv('BOT_TOKEN'),
            admin_id=int(getenv('ADMIN_ID'))
        )
    )
