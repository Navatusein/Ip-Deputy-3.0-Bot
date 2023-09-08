from . import client

from bot.models.student_settings import StudentSettings


class StudentService:
    @staticmethod
    def get_settings(telegram_id: int) -> StudentSettings | None:
        response = client.get("/student/settings", params={"telegramId": telegram_id})
        response.raise_for_status()

        if response.status_code == 204:
            return None

        return StudentSettings.from_dict(response.json())

    @staticmethod
    def update_settings(settings: StudentSettings) -> StudentSettings:
        response = client.put("/student/settings", json=settings.to_dict())
        response.raise_for_status()
        return StudentSettings.from_dict(response.json())
