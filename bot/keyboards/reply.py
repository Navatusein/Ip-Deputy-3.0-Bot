from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("↩ Назад"))],
        ],
        resize_keyboard=True
    )


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
        ],
        resize_keyboard=True
    )

def back_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
            [KeyboardButton(text=_("↩ Назад"))],
        ],
        resize_keyboard=True
    )


def login_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_('🔐 Авторизуватися'), request_contact=True)]
        ],
        resize_keyboard=True
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("🗓 Розклад")), KeyboardButton(text=_("🧾 Захист робіт"))],
            [KeyboardButton(text=_("🗒 Інформація"))],
            # [KeyboardButton(text=_("☎️ Зв'язок")), KeyboardButton(text=_("🗒 Інформація"))],
            [KeyboardButton(text=_("⚙ Налаштування"))]
        ],
        resize_keyboard=True
    )


def schedule_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
            [KeyboardButton(text=_("🕐 Сьогодні")), KeyboardButton(text=_("🕑 Завтра"))],
            [KeyboardButton(text=_("🕐 Цей тиждень")), KeyboardButton(text=_("🕑 Наступний тиждень"))],
        ],
        resize_keyboard=True
    )


def information_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
            [KeyboardButton(text=_("🧑‍🎓 Студенти")), KeyboardButton(text=_("🧑🏻‍🏫 Викладачі"))],
            [KeyboardButton(text=_("📖 Предмети")), KeyboardButton(text=_("🌐 Посилання"))],
        ],
        resize_keyboard=True
    )


def settings_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
            [KeyboardButton(text=_("🇺🇦 Мова"))],
            [KeyboardButton(text=_("🗓 Формат розкладу"))],
            [KeyboardButton(text=_("🔔 Нагадувати дедлайни"))],
        ],
        resize_keyboard=True
    )


def submission_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("📋 Головне меню"))],
            [KeyboardButton(text=_("➕ Записатись")), KeyboardButton(text=_("🧾 Мої записи"))],
            [KeyboardButton(text=_("🗳 Отримати список"))],
        ],
        resize_keyboard=True
    )