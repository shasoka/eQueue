#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

import requests
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User
from core.schemas.moodle import (
    EcoursesSubjectDescription,
    EcourseSubjectModule,
    EcoursesSubjectStructure,
)
from core.schemas.subjects import WorkspaceSubjectCreate
from crud.workspaces import get_workspace_subject_ids
from utils import validate


async def user_enrolled_courses(
    token: str,
    user: User,
    session: AsyncSession,
) -> list[WorkspaceSubjectCreate]:
    response = requests.post(
        settings.moodle.enrolled_courses_url % (token, user.ecourses_user_id)
    )
    if not isinstance(response, list):
        await validate(response.json())

    courses = []
    for course in response.json():
        if course["lastaccess"] is None:
            course["lastaccess"] = -1
        if course["id"] not in await get_workspace_subject_ids(
            session, user.assigned_workspace_id
        ):
            courses.append(EcoursesSubjectDescription.model_validate(course))

    sorted_courses = sorted(
        courses,
        key=lambda c: (
            c.hidden,
            -c.lastaccess,
            not c.isfavourite,
        ),
    )

    casted_courses = []
    for course in sorted_courses:
        casted_courses.append(
            WorkspaceSubjectCreate(
                workspace_id=user.assigned_workspace_id,
                ecourses_id=course.id,
                name=course.shortname,
                ecourses_link=settings.moodle.course_url % course.id,
                professor=None,
                professor_contact=None,
                requirements=None,
            )
        )

    return casted_courses


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


async def check_course_availability(
    course_id: int,
    token: str,
) -> bool:
    response = requests.post(settings.moodle.course_structure % (token, course_id))
    return isinstance(response, list)
