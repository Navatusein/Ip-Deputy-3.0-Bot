import pytz

from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import Config
from bot.filters.is_authorized import IsAuthorized
from bot.models.student_settings import StudentSettings
from bot.utilities.format_schedule_message import format_day_schedule_message, format_week_schedule_message

router = Router()


@router.message(Command("today"), IsAuthorized())
async def today_schedule(message: Message, configs: Config) -> None:
    date = datetime.now(pytz.timezone(configs.time_zone))
    schedule = format_day_schedule_message(message.from_user.id, date)
    await message.answer(schedule, disable_web_page_preview=True)


@router.message(Command("tomorrow"), IsAuthorized())
async def tomorrow_schedule(message: Message, configs: Config) -> None:
    date = datetime.now(pytz.timezone(configs.time_zone)) + timedelta(days=1)
    schedule = format_day_schedule_message(message.from_user.id, date)
    await message.answer(schedule, disable_web_page_preview=True)


@router.message(Command("this_week"), IsAuthorized())
async def today_week_schedule(message: Message, cache: dict[str, str]) -> None:
    compact = False

    json = cache.get(f"student_settings:{message.from_user.id}")
    if json is not None:
        settings: StudentSettings = StudentSettings.from_json(json)
        compact = settings.schedule_compact

    date = datetime.today()
    schedule = format_week_schedule_message(message.from_user.id, date, compact)
    await message.answer(schedule, disable_web_page_preview=True)


@router.message(Command("next_week"), IsAuthorized())
async def tomorrow_week_schedule(message: Message, cache: dict[str, str]) -> None:
    compact = False

    json = cache.get(f"student_settings:{message.from_user.id}")
    if json is not None:
        settings: StudentSettings = StudentSettings.from_json(json)
        compact = settings.schedule_compact

    date = datetime.today() + timedelta(days=7 - datetime.today().weekday())
    schedule = format_week_schedule_message(message.from_user.id, date, compact)
    await message.answer(schedule, disable_web_page_preview=True)
