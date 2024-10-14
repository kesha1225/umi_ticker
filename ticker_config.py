import os
import typing

from dotenv import load_dotenv

load_dotenv()


def get_env_value(key: str) -> str | typing.NoReturn:
    return os.environ[key]


CMC_API_KEY: str = get_env_value("CMC_API_KEY")
BOT_TOKEN: str = get_env_value("BOT_TOKEN")
UMI_GAME_BOT_DB_URL: str = get_env_value("UMI_GAME_BOT_DB_URL")

GROUP_ID = -1001743072181
