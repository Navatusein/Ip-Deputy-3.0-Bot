from typing import Any

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from bot.filters.is_authorized import IsAuthorized
from bot.keyboards.reply import back_main_keyboard
from bot.models.student_settings import StudentSettings
from bot.services.student_service import StudentService

router = Router()


class SettingsStatesGroup(StatesGroup):
    language = State()
    compact_schedule = State()
    remind_deadlines = State()


@router.message(F.text == __("🇺🇦 Мова"), IsAuthorized())
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    settings_data = [
        {"text": "🇺🇦 Українська", "value": "uk"},
        {"text": "💩 Русский", "value": "ru"},
    ]
    keyboard_buttons = [[KeyboardButton(text=_("↩ Назад"))]]
    keyboard_buttons += [[KeyboardButton(text=value["text"])] for value in settings_data]

    await state.clear()
    await state.set_state(SettingsStatesGroup.language)
    await state.set_data({"settings_data": settings_data})

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    setting = next(value for value in settings_data if value["value"] == settings.language)
    status_message = _("Поточне значення: {value}").format(value=setting["text"])

    await message.answer(status_message,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(SettingsStatesGroup.language)
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    data = await state.get_data()
    settings_data: list[dict[str, str]] = data["settings_data"]
    setting = next((value for value in settings_data if value["text"] == message.text), None)

    if setting is None:
        await message.answer(_("Не коректне введення!"))
        return

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    settings.language = setting["value"]

    cache[f"student_settings:{message.from_user.id}"] = StudentService.update_settings(settings).to_json()

    await message.answer(text=_("Значення змінено на: {value}").format(value=setting["text"]))


@router.message(F.text == __("🗓 Формат розкладу"), IsAuthorized())
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    settings_data = [
        {"text": "➡️⬅️ Компактний", "value": True},
        {"text": "⬅️➡️ Повноцінний", "value": False},
    ]
    keyboard_buttons = [[KeyboardButton(text=_("↩ Назад"))]]
    keyboard_buttons += [[KeyboardButton(text=value["text"])] for value in settings_data]

    await state.clear()
    await state.set_state(SettingsStatesGroup.compact_schedule)
    await state.set_data({"settings_data": settings_data})

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    setting = next(value for value in settings_data if value["value"] == settings.schedule_compact)
    status_message = _("Поточне значення: {value}").format(value=setting["text"])

    await message.answer(status_message,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(SettingsStatesGroup.compact_schedule)
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    data = await state.get_data()
    settings_data: list[dict[str, str]] = data["settings_data"]
    setting = next((value for value in settings_data if value["text"] == message.text), None)

    if setting is None:
        await message.answer(_("Не коректне введення!"))
        return

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    settings.schedule_compact = setting["value"]

    cache[f"student_settings:{message.from_user.id}"] = StudentService.update_settings(settings).to_json()

    await message.answer(text=_("Значення змінено на: {value}").format(value=setting["text"]))


@router.message(F.text == __("🔔 Нагадувати дедлайни"), IsAuthorized())
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    settings_data = [
        {"text": "🔔 Нагадувати", "value": True},
        {"text": "🔕 Не турбувати", "value": False},
    ]
    keyboard_buttons = [[KeyboardButton(text=_("↩ Назад"))]]
    keyboard_buttons += [[KeyboardButton(text=value["text"])] for value in settings_data]

    await state.clear()
    await state.set_state(SettingsStatesGroup.remind_deadlines)
    await state.set_data({"settings_data": settings_data})

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    setting = next(value for value in settings_data if value["value"] == settings.remind_deadlines)
    status_message = _("Поточне значення: {value}").format(value=setting["text"])

    await message.answer(status_message,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(SettingsStatesGroup.remind_deadlines)
async def handler(message: Message, state: FSMContext, cache: dict[str, str]) -> None:
    data = await state.get_data()
    settings_data: list[dict[str, str]] = data["settings_data"]
    setting = next((value for value in settings_data if value["text"] == message.text), None)

    if setting is None:
        await message.answer(_("Не коректне введення!"))
        return

    settings: StudentSettings = StudentSettings.from_json(cache[f"student_settings:{message.from_user.id}"])
    settings.remind_deadlines = setting["value"]

    cache[f"student_settings:{message.from_user.id}"] = StudentService.update_settings(settings).to_json()

    await message.answer(text=_("Значення змінено на: {value}").format(value=setting["text"]))
