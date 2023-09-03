from . import client

from bot.models.schedule_day import ScheduleDay
from bot.models.schedule_week import ScheduleWeek


class ScheduleService:
    @staticmethod
    def get_day_schedule(telegram_id: int, date: str) -> ScheduleDay | None:
        response = client.get("/schedule/day", params={"telegramId": telegram_id, "dateString": date})
        response.raise_for_status()

        if response.status_code == 204:
            return None

        return ScheduleDay.from_dict(response.json())

    @staticmethod
    def get_week_schedule(telegram_id: int, date: str) -> ScheduleWeek | None:
        response = client.get("/schedule/week", params={"telegramId": telegram_id, "dateString": date})
        response.raise_for_status()

        if response.status_code == 204:
            return None

        return ScheduleWeek.from_dict(response.json())
