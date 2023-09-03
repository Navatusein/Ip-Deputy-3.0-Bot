from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.filters.is_authorized import IsAuthorized
from bot.keyboards.reply import main_menu_keyboard

router = Router()


@router.message(Command("start"), IsAuthorized())
async def start_command(message: Message) -> None:
    await message.answer(_("📋 Головне меню"), reply_markup=main_menu_keyboard())
