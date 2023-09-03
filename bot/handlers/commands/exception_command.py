from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message(Command("exception"))
async def exception_command(message: Message) -> None:
    raise RuntimeError("Exception exception_command")
