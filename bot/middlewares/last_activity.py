from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.services.student_service import StudentService


class LastActivity(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        StudentService.update_last_activity(event.from_user.id)
        return await handler(event, data)
