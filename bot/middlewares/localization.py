from typing import Dict, Any

from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware

from bot.models.student_settings import StudentSettings


class Localization(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        user: User = data["event_from_user"]
        cache: Dict[str, str] = data["cache"]

        # Try to get user settings from cache
        json = cache.get(f"student_settings:{user.id}")

        # If user settings is none it means that user is not authorized
        if json is not None:
            settings: StudentSettings = StudentSettings.from_json(json)
            return settings.language

        return "uk"
