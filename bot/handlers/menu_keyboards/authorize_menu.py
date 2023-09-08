import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.markdown import hcode

from bot.services.authentication_service import AuthenticationService
from bot.keyboards.reply import main_menu_keyboard
from bot.models.student_contact import StudentContact

router = Router()


class AuthorizeStatesGroup(StatesGroup):
    contact = State()


@router.message(AuthorizeStatesGroup.contact, F.content_type == "contact")
async def handler(message: Message, state: FSMContext) -> None:
    telegram_id: int = message.from_user.id
    phone: str = str(int(message.contact.phone_number))

    # Check if user send his contact
    if message.contact.user_id != telegram_id:
        await message.answer(_("Це не ваш контакт!"))
        logging.warning(f"Student id: {telegram_id} name: {message.from_user.username} sent the wrong contact")
        return

    contact: StudentContact = StudentContact(telegram_id=telegram_id, phone=phone)

    # Send request to the API to authorize user
    result, code = AuthenticationService.authorize(contact)

    # Check if user exist in database
    if not result:
        await message.answer(_("Вас немає у базі даних!\nНапишіть @Navatusein код помилки: {}").format(hcode(code)))
        logging.warning(f"[{code}] No such student in database id: {telegram_id} phone: {message.from_user.username} "
                        f"name: {message.from_user.username} sent the wrong contact")
        return

    await message.answer(_('Авторизація виконана успішно!'), reply_markup=main_menu_keyboard())
    await state.clear()
