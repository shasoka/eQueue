#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

import requests

from core.config import settings
from core.schemas.moodle import (
    EcoursesSubjectDescription,
    EcourseSubjectModule,
    EcoursesSubjectStructure,
)
from utils import validate


async def user_enrolled_courses(
    token: str,
    ecourses_user_id: int,
) -> list[EcoursesSubjectDescription]:
    response = requests.post(
        settings.moodle.enrolled_courses_url % (token, ecourses_user_id)
    )
    if not isinstance(response, list):
        await validate(response.json())

    result = []
    for course in response.json():
        result.append(EcoursesSubjectDescription.model_validate(course))

    return result


async def get_course_data(
    course_id: int,
    token: str,
) -> EcoursesSubjectStructure | None:
    response = requests.post(settings.moodle.course_structure % (token, course_id))
    if not isinstance(response, list):
        await validate(response.json())

    result = []
    for structure_node in response.json():
        for module in structure_node["modules"]:
            if module["modname"] == "assign":
                result.append(EcourseSubjectModule.model_validate(module))

    return EcoursesSubjectStructure.model_validate({"assign_modules": result})
