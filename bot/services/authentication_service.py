from . import client

from bot.models.student_contact import StudentContact


class AuthenticationService:
    @staticmethod
    def authorize(contact: StudentContact) -> [bool, str | None]:
        response = client.post("/authentication/authorize", json=contact.to_dict())
        response.raise_for_status()

        if response.text != "Ok":
            return False, response.text

        return True, ""
