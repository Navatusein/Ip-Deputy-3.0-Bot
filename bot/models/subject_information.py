from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SubjectInformation(DataClassJsonMixin):
    name: str
    short_name: str
    laboratory_days_count: int
    practical_days_count: int
    lectures_days_count: int
    laboratory_count: int
    practical_count: int
