from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase

from bot.models.couple_data import CoupleData
from bot.models.schedule_day import ScheduleDay


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ScheduleWeek(DataClassJsonMixin):
    couple_times: list[str]
    schedule_days: list[ScheduleDay]
