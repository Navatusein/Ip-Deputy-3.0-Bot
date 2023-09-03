from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, config, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StudentSettings(DataClassJsonMixin):
    telegram_id: int
    language: str
    schedule_compact: bool
    remind_deadlines: bool
