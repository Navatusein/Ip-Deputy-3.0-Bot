from . import client

from bot.models.student_information import StudentInformation
from bot.models.teacher_information import TeacherInformation
from bot.models.subject_information import SubjectInformation
from bot.models.link_information import LinkInformation


class InformationService:
    @staticmethod
    def get_students_information() -> list[StudentInformation]:
        response = client.get("/information/students")
        response.raise_for_status()
        return [StudentInformation.from_dict(value) for value in response.json()]

    @staticmethod
    def get_teachers_information() -> list[TeacherInformation]:
        response = client.get("/information/teachers")
        response.raise_for_status()
        return [TeacherInformation.from_dict(value) for value in response.json()]

    @staticmethod
    def get_subjects_information() -> list[SubjectInformation]:
        response = client.get("/information/subjects")
        response.raise_for_status()
        return [SubjectInformation.from_dict(value) for value in response.json()]

    @staticmethod
    def get_links_information() -> list[LinkInformation]:
        response = client.get("/information/links")
        response.raise_for_status()
        return [LinkInformation.from_dict(value) for value in response.json()]
