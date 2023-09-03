from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _

from bot.filters.is_authorized import IsAuthorized
from bot.keyboards.reply import back_main_keyboard
from bot.models.link_information import LinkInformation
from bot.models.student_information import StudentInformation
from bot.models.subject_information import SubjectInformation
from bot.models.teacher_information import TeacherInformation
from bot.services.information_service import InformationService

router = Router()


class StudentStatesGroup(StatesGroup):
    select = State()


class TeacherStatesGroup(StatesGroup):
    select = State()


class SubjectStatesGroup(StatesGroup):
    select = State()


class LinksStatesGroup(StatesGroup):
    select = State()


@router.message(F.text == __("🧑‍🎓 Студенти"), IsAuthorized())
@router.message(StudentStatesGroup.select, F.text == __("↩ Назад"))
async def handler(message: Message, state: FSMContext) -> None:
    students = InformationService.get_students_information()
    keyboard_buttons = [[KeyboardButton(text=_("📋 Головне меню"))]]
    keyboard_buttons += [[KeyboardButton(text=value.full_name)] for value in students]

    await state.clear()
    await state.set_state(StudentStatesGroup.select)
    await state.set_data({"students": students})

    await message.answer(message.text,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(StudentStatesGroup.select)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    students: list[StudentInformation] = data["students"]
    student = next((value for value in students if value.full_name == message.text), None)

    if student is None:
        await message.answer(_("Не коректне введення!"))
        return

    student_message = f"<b>{student.full_name}</b>:\n\n"
    student_message += _("Підгрупа: {subgroup}\n").format(subgroup=student.subgroup)
    student_message += _("Номер телефону: +{contact_phone}\n").format(contact_phone=student.contact_phone)
    student_message += _("Пошта: {email}\n").format(email=student.email)
    student_message += _("Фітовська пошта: {fit_email}\n").format(fit_email=student.fit_email)
    student_message += _("Нік в телеграм: {telegram_nickname}\n").format(telegram_nickname=student.telegram_nickname)
    student_message += _("День народження: {birthday}\n").format(birthday=student.birthday)

    await message.answer(student_message, reply_markup=back_main_keyboard())
    await message.bot.send_contact(chat_id=message.chat.id, phone_number=student.telegram_phone,
                                   first_name=student.name, last_name=student.surname)


@router.message(F.text == __("🧑🏻‍🏫 Викладачі"), IsAuthorized())
@router.message(TeacherStatesGroup.select, F.text == __("↩ Назад"))
async def handler(message: Message, state: FSMContext) -> None:
    teachers = InformationService.get_teachers_information()
    keyboard_buttons = [[KeyboardButton(text=_("📋 Головне меню"))]]
    keyboard_buttons += [[KeyboardButton(text=value.full_name)] for value in teachers]

    await state.clear()
    await state.set_state(TeacherStatesGroup.select)
    await state.set_data({"teachers": teachers})

    await message.answer(message.text,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(TeacherStatesGroup.select)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    teachers: list[TeacherInformation] = data["teachers"]
    teacher = next((value for value in teachers if value.full_name == message.text), None)

    if teacher is None:
        await message.answer(_("Не коректне введення!"))
        return

    teacher_message = f"<b>{teacher.full_name}</b>:\n\n"
    teacher_message += _("Номер телефону: +{contact_phone}\n").format(contact_phone=teacher.contact_phone)
    teacher_message += _("Пошта: {email}\n").format(email=teacher.email)
    teacher_message += _("Фітовська пошта: {fit_email}\n").format(fit_email=teacher.fit_email)
    teacher_message += _("Нік в телеграм: {telegram_nickname}\n").format(telegram_nickname=teacher.telegram_nickname)

    await message.answer(teacher_message, reply_markup=back_main_keyboard())


@router.message(F.text == __("📖 Предмети"), IsAuthorized())
@router.message(SubjectStatesGroup.select, F.text == __("↩ Назад"))
async def handler(message: Message, state: FSMContext) -> None:
    subjects = InformationService.get_subjects_information()
    keyboard_buttons = [[KeyboardButton(text=_("📋 Головне меню"))]]
    keyboard_buttons += [[KeyboardButton(text=value.name)] for value in subjects]

    await state.clear()
    await state.set_state(SubjectStatesGroup.select)
    await state.set_data({"subjects": subjects})

    await message.answer(message.text,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(SubjectStatesGroup.select)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    subjects: list[SubjectInformation] = data["subjects"]
    subject = next((value for value in subjects if value.name == message.text), None)

    if subject is None:
        await message.answer(_("Не коректне введення!"))
        return

    teacher_message = f"<b>{subject.name}</b>:\n\n"
    teacher_message += (_("Коротка назва: {short_name}\n")
                        .format(short_name=subject.short_name))
    teacher_message += (_("Кількість лекційних днів: {lectures_days_count}\n")
                        .format(lectures_days_count=subject.lectures_days_count))
    teacher_message += (_("Кількість практичних днів: {practical_days_count}\n")
                        .format(practical_days_count=subject.practical_days_count))
    teacher_message += (_("Кількість лабораторних днів: {laboratory_days_count}\n")
                        .format(laboratory_days_count=subject.laboratory_days_count))

    await message.answer(teacher_message, reply_markup=back_main_keyboard())


@router.message(F.text == __("🌐 Посилання"), IsAuthorized())
async def handler(message: Message, state: FSMContext) -> None:
    links = InformationService.get_links_information()
    keyboard_buttons = [[KeyboardButton(text=_("📋 Головне меню"))]]
    keyboard_buttons += [[KeyboardButton(text=value.name)] for value in links]

    await state.clear()
    await state.set_state(LinksStatesGroup.select)
    await state.set_data({"links": links})

    await message.answer(message.text,
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))


@router.message(LinksStatesGroup.select)
async def handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    links: list[LinkInformation] = data["links"]
    link = next((value for value in links if value.name == message.text), None)

    if link is None:
        await message.answer(_("Не коректне введення!"))
        return

    teacher_message = f"<b>{link.name}</b>:\n\n{link.description}"
    link_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=link.name, url=link.url)]])

    await message.answer(teacher_message, reply_markup=link_menu)
