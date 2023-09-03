from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LinkInformation(DataClassJsonMixin):
    name: str
    description: str
    url: str
