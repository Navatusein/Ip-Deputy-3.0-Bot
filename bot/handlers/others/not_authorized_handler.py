from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.is_authorized import IsAuthorized
from bot.handlers.menu_keyboards.authorize_menu import AuthorizeStatesGroup
from bot.keyboards.reply import login_menu_keyboard

from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(~IsAuthorized())
async def handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AuthorizeStatesGroup.contact)
    await message.reply(text=_('Необхідно авторизуватися!'), reply_markup=login_menu_keyboard())
