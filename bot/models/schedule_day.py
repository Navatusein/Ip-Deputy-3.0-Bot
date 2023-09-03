from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase

from bot.models.couple_data import CoupleData


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ScheduleDay(DataClassJsonMixin):
    date: str
    couples: list[CoupleData]
