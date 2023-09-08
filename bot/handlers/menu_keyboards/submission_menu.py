import collections

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from bot.filters.is_authorized import IsAuthorized
from bot.keyboards.reply import main_keyboard, submission_menu_keyboard
from bot.models.submission import Submission
from bot.models.submissions_config import SubmissionsConfig
from bot.services.submission_service import SubmissionService
from bot.utilities.web_app import create_web_app_keyboard

router = Router()


class GetSubmissionStatesGroup(StatesGroup):
    subject = State()
    type = State()
    subgroup = State()


@router.message(F.text == __("➕ Записатись"), IsAuthorized())
async def handler(message: Message) -> None:
    keyboard = create_web_app_keyboard("/submission/register")

    message_string = ''
    message_string += _("➕ Записатись") + '\n'
    message_string += _("Натисніть на кнопку щоб відкрити інтерфейс 👇")

    await message.answer(message_string, reply_markup=keyboard)


@router.message(F.text == __("🧾 Мої записи"), IsAuthorized())
async def handler(message: Message) -> None:
    keyboard = create_web_app_keyboard("/submission/control")

    message_string = ''
    message_string += _("🧾 Мої записи") + '\n'
    message_string += _("Натисніть на кнопку щоб відкрити інтерфейс 👇")

    await message.answer(message_string, reply_markup=keyboard)


@router.message(GetSubmissionStatesGroup.type, F.text == __("↩ Назад"))
@router.message(F.text == __("🗳 Отримати список"), IsAuthorized())
async def handler(message: Message, state: FSMContext) -> None:
    submissions_configs: list[SubmissionsConfig] = SubmissionService.get_submissions_configs()

    names = {item.name for item in submissions_configs}

    keyboard_buttons = [[KeyboardButton(text=_("📋 Головне меню"))]]
    keyboard_buttons += [[KeyboardButton(text=value)] for value in names]

    await state.clear()
    await state.set_state(GetSubmissionStatesGroup.subject)
    await state.set_data({"submissions_configs": submissions_configs})

    await message.answer(message.text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(GetSubmissionStatesGroup.subgroup, F.text == __("↩ Назад"))
@router.message(GetSubmissionStatesGroup.subject)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    submissions_configs: list[SubmissionsConfig] = data["submissions_configs"]
    name = message.text

    if message.text == _("↩ Назад"):
        name: str = data["name"]

    types = {item.type for item in filter(lambda x: x.name == name, submissions_configs)}

    if types == set():
        await message.answer(_("Не коректне введення!"))
        return

    await state.set_state(GetSubmissionStatesGroup.type)
    await state.set_data({
        "submissions_configs": submissions_configs,
        "name": message.text
    })

    keyboard_buttons = [[KeyboardButton(text=_("↩ Назад"))]]
    keyboard_buttons += [[KeyboardButton(text=value)] for value in types]

    await message.answer(message.text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(GetSubmissionStatesGroup.type)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    submissions_configs: list[SubmissionsConfig] = data["submissions_configs"]
    name: str = data["name"]

    filtered_submissions_configs = list(filter(lambda x: x.name == name and x.type == message.text, submissions_configs))

    if len(filtered_submissions_configs) == 0:
        await message.answer(_("Не коректне введення!"))
        return

    if filtered_submissions_configs[0].subgroup is None:
        await state.clear()
        message_string = format_submission_message(filtered_submissions_configs[0].submissions, message.text)
        await message.answer(message_string, reply_markup=submission_menu_keyboard())
        return

    await state.set_state(GetSubmissionStatesGroup.subgroup)
    await state.set_data({
        "submissions_configs": submissions_configs,
        "name": name,
        "type": message.text
    })

    keyboard_buttons = [[KeyboardButton(text=_("↩ Назад"))]]
    keyboard_buttons += [[KeyboardButton(text=value.subgroup)] for value in filtered_submissions_configs]

    await message.answer(message.text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(GetSubmissionStatesGroup.subgroup)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    submissions_configs: list[SubmissionsConfig] = data["submissions_configs"]
    name: str = data["name"]
    type: str = data["type"]

    submissions_config = next((value for value in submissions_configs if value.name == name and
                               value.type == type and value.subgroup == message.text), None)

    if submissions_config is None:
        await message.answer(_("Не коректне введення!"))
        return

    await state.clear()
    message_string = format_submission_message(submissions_config.submissions, type)
    await message.answer(message_string, reply_markup=submission_menu_keyboard())


def format_submission_message(submissions: list[Submission], type: str) -> str:
    message = ""
    students = list(dict.fromkeys([x.student for x in submissions]))

    if len(students) == 0:
        return _("На захист ніхто не записався")

    for index, student in enumerate(students):
        student_submissions = list(filter(lambda x: x.student == student, submissions))

        message += f"{index + 1}) {student} ({type}): {', '.join([value.name for value in student_submissions])};\n"

    return message
