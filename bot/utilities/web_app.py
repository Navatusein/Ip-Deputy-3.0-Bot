from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.config import load_config

configs = load_config()


def create_web_app_keyboard(url: str) -> InlineKeyboardMarkup:
    web_app = WebAppInfo(url=f"{configs.frontend_url}/bot{url}")

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("Відкрити інтерфейс"), web_app=web_app)]
    ], resize_keyboard=True)

    return inline_keyboard
