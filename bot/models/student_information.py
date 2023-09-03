from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StudentInformation(DataClassJsonMixin):
    name: str
    surname: str
    patronymic: str
    subgroup: str | None
    contact_phone: str | None
    telegram_phone: str
    email: str
    fit_email: str
    telegram_nickname: str | None
    birthday: str

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name}"
