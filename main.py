import asyncio
import logging

from logging import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, ConstI18nMiddleware

from bot.config import load_config
from bot.middlewares.localization import Localization
from bot.handlers.commands import start_command, exception_command, test_command, schedule_commands
from bot.handlers.others import not_authorized_handler, exceptions_handler
from bot.handlers.menu_keyboards import (authorize_menu, main_manu, schedule_menu, information_menu, settings_menu,
                                         submission_menu)


def on_startup(dispatcher: Dispatcher) -> None:
    logging.info("Bot started!")


async def main() -> None:
    configs = load_config()
    dp = Dispatcher()

    dp.startup.register(on_startup)

    i18n = I18n(path="locales", default_locale="uk", domain="default")

    # I18n Localization middleware
    dp.message.middleware(Localization(i18n=i18n))
    dp.message.outer_middleware(Localization(i18n=i18n))
    # dp.message.outer_middleware(ConstI18nMiddleware(locale="uk", i18n=i18n))

    # Command handlers
    dp.include_routers(start_command.router, exception_command.router, test_command.router,
                       schedule_commands.router)

    # Menu handlers
    dp.include_routers(authorize_menu.router, main_manu.router, schedule_menu.router, information_menu.router,
                       settings_menu.router, submission_menu.router)

    # Other handlers
    dp.include_router(not_authorized_handler.router)

    # Exception handler
    dp.include_router(exceptions_handler.router)

    logging.config.dictConfig(configs.logger_settings)

    bot = Bot(configs.bot_token, parse_mode=ParseMode.HTML)

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Показати головне меню"),
            BotCommand(command="today", description="Отримати розклад на сьогодні"),
            BotCommand(command="tomorrow", description="Отримати розклад на завтра"),
            BotCommand(command="today_week", description="Отримати розклад на цей тиждень"),
            BotCommand(command="tomorrow_week", description="Отримати розклад на настурний тиждень"),
        ]
    )
    await dp.start_polling(bot, cache={}, i18n=i18n)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
