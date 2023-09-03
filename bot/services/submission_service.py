from . import client

from bot.models.submissions_config import SubmissionsConfig


class SubmissionService:
    @staticmethod
    def get_submissions_configs() -> list[SubmissionsConfig] | None:
        response = client.get("/submission/submissions-configs")
        response.raise_for_status()

        return [SubmissionsConfig.from_dict(value) for value in response.json()]
