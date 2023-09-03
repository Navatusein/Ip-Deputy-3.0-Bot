from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import lazy_gettext as __

from bot.filters.is_authorized import IsAuthorized
from bot.keyboards.reply import

router = Router()

@router.message(F.text == __(""), IsAuthorized())
async def handler(message: Message) -> None:
    await message.answer(message.text, reply_markup=)