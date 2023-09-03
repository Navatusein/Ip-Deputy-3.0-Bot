import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.filters import StateFilter

from bot.filters.is_authorized import IsAuthorized
from bot.handlers.menu_keyboards.settings_menu import SettingsStatesGroup
from bot.keyboards.reply import (main_menu_keyboard, schedule_menu_keyboard, information_menu_keyboard,
                                 settings_menu_keyboard, submission_menu_keyboard)

router = Router()


@router.message(StateFilter(None), F.text == __("↩ Назад"), IsAuthorized())
@router.message(F.text == __("📋 Головне меню"), IsAuthorized())
async def handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(message.text, reply_markup=main_menu_keyboard())


@router.message(F.text == __("🗓 Розклад"), IsAuthorized())
async def handler(message: Message) -> None:
    await message.answer(message.text, reply_markup=schedule_menu_keyboard())


@router.message(F.text == __("🗒 Інформація"), IsAuthorized())
async def handler(message: Message) -> None:
    await message.answer(message.text, reply_markup=information_menu_keyboard())


@router.message(StateFilter(SettingsStatesGroup), F.text == __("↩ Назад"), IsAuthorized())
@router.message(F.text == __("⚙ Налаштування"), IsAuthorized())
async def handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(message.text, reply_markup=settings_menu_keyboard())


@router.message(F.text == __("🧾 Захист робіт"), IsAuthorized())
async def handler(message: Message) -> None:
    await message.answer(message.text, reply_markup=submission_menu_keyboard())
