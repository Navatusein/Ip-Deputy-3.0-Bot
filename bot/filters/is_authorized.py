import logging

from aiogram.filters import Filter
from aiogram.types import Message

from bot.services.student_service import StudentService


class IsAuthorized(Filter):
    async def __call__(self, message: Message, cache: dict[str, str]) -> bool:
        # Try to get user setting from cache
        json = cache.get(f"student_settings:{message.from_user.id}")
        if json is None:
            # Send request to API to get user settings
            settings = StudentService.get_settings(message.from_user.id)

            # If settings is none it means that user not authorized
            if settings is None:
                return False

            # Save user settings to cache
            cache[f"student_settings:{message.from_user.id}"] = settings.to_json()
            logging.info(f"Cache added student_settings:{message.from_user.id} with:{settings}")

        return True
