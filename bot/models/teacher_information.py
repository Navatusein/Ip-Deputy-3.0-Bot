from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TeacherInformation(DataClassJsonMixin):
    name: str
    surname: str
    patronymic: str
    contact_phone: str | None
    email: str | None
    fit_email: str | None
    telegram_nickname: str | None

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"
