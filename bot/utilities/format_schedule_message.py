from datetime import datetime

from aiogram.utils.i18n import gettext as _
from aiogram.utils.markdown import hlink

from bot.misc.emoji import number_emoji
from bot.models.couple_data import CoupleData
from bot.models.schedule_day import ScheduleDay
from bot.services.schedule_service import ScheduleService


def format_day_schedule_message(telegram_id: int, date: datetime) -> str:
    schedule_day = ScheduleService.get_day_schedule(telegram_id, date.strftime("%Y-%m-%d"))
    message = ""

    if date.date() == datetime.today().date():
        message += _("<b>Розклад на сьогодні ({date}):</b>\n").format(date=schedule_day.date)
    else:
        message += _("<b>Розклад на завтра ({date}):</b>\n").format(date=schedule_day.date)

    message += format_day_couples(schedule_day)

    return message


def format_week_schedule_message(telegram_id: int, date: datetime, compact: bool = False) -> str:
    schedule_week = ScheduleService.get_week_schedule(telegram_id, date.strftime("%Y-%m-%d"))
    days_of_week = [_("ПОНЕДІЛОК"), _("ВІВТОРОК"), _("СЕРЕДА"), _("ЧЕТВЕР"), _("П'ЯТНИЦЯ"), _('СУБОТА'), _('НЕДІЛЯ')]
    message = ""

    if date.date() == datetime.today().date():
        message += _(f'<b>📅 Розклад на цей тиждень:</b>\n\n')
    else:
        message += _(f'<b>📅 Розклад на наступний тиждень:</b>\n\n')

    if compact:
        message += _(f'<b>Час пар:</b>\n')

        for index, value in enumerate(schedule_week.couple_times):
            message += f'{number_emoji[index + 1]} {value}\n'

        message += '\n'

    for index, schedule_day in enumerate(schedule_week.schedule_days):
        message += f'<b>{days_of_week[index]} ({schedule_day.date}):</b>\n'
        message += format_day_couples(schedule_day, not compact)
        message += "\n"

    return message


def format_day_couples(schedule: ScheduleDay, show_time: bool = True) -> str:
    day_string = ""

    my_subgroup_couple = list(filter(lambda x: x.is_my_subgroup, schedule.couples))

    for couple in my_subgroup_couple:
        day_string += format_couple_string(couple, show_time)

    other_subgroup_couple = list(filter(lambda x: not x.is_my_subgroup, schedule.couples))

    if len(other_subgroup_couple):
        day_string += _("\n🚷 <i>Пари у іншої підгрупи:</i>\n")

        for couple in other_subgroup_couple:
            day_string += f"<i>{format_couple_string(couple, show_time)}</i>"

    if len(schedule.couples) == 0:
        day_string += f"{_('🛌 Пар немає, відпочивай!')}\n"

    return day_string


def format_couple_string(couple: CoupleData, show_time: bool) -> str:
    if couple.couple_index is None:
        couple_string = _("⚠️ Нестандартний час:\n➖ [{time}]").format(time=couple.time)
    else:
        couple_string = f"{number_emoji[couple.couple_index + 1]} "

        if show_time:
            couple_string += f"[{couple.time}]"

    if couple.link is not None:
        couple_string += hlink(couple.subject, couple.link)
    else:
        couple_string += couple.subject

    couple_string += f" ({couple.subject_type})"

    if couple.cabinet is not None:
        couple_string += f" {couple.cabinet} {_('кб.')}"

    return f"{couple_string}\n"
