import logging
import uuid

from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent

from aiogram.utils.i18n import gettext as _, I18n
from httpx import ConnectError, ReadTimeout

router = Router()


# Handler for request timeout to API
@router.error(ExceptionTypeFilter(ConnectError, ReadTimeout), F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message, i18n: I18n):
    logging.critical("Connection to backend timeout!")
    await message.answer(i18n.gettext("Упс, не можу під'єднатись до сервера!\nВикликайте фіксиків!"))


# Handler for unhandled exceptions
@router.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message, i18n: I18n):
    code = uuid.uuid4().hex[:10].lower()
    logging.critical("[%s] Unhandled error: %s",code, event.exception, exc_info=True)
    await message.answer(i18n.gettext("Упс, щось пішло не так.\nКод помилки: <code>{code}</code>").format(code=code))
