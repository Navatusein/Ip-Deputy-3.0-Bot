from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CoupleData(DataClassJsonMixin):
    subject: str
    subject_type: str
    couple_index: int | None
    is_my_subgroup: bool
    time: str | None
    link: str | None
    subject: str | None
    cabinet: str | None
    additional_information: str | None
