from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase

from bot.models.submission import Submission


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SubmissionsConfig(DataClassJsonMixin):
    id: int
    name: str
    type: str
    subgroup: str | None
    submissions: list[Submission]
