import json

from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin


@dataclass_json
@dataclass
class Config(DataClassJsonMixin):
    bot_token: str
    logger_settings: dict
    api_token: str
    api_url: str
    frontend_url: str
    time_zone: str


def load_config() -> Config:
    # Loading configs from json file
    with open("config/config.json") as json_file:
        return Config.from_dict(json.load(json_file))
