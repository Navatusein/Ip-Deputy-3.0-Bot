from datetime import date, datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.services.information_service import InformationService
from bot.services.schedule_service import ScheduleService

router = Router()


@router.message(Command("test"))
async def test_command(message: Message) -> None:
    print(InformationService.get_students_information())
