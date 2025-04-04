#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from urllib.parse import quote_plus as url_encode

import requests
from core.config import settings
from core.models import User
from core.schemas.moodle import (
    EcoursesSubjectDescription,
)
from core.schemas.subject_assignments import SubjectAssignmentCreate
from core.schemas.subjects import WorkspaceSubjectCreate, WorkspaceSubjectRead
from crud.workspaces import get_workspace_subject_ids_and_names
from fastapi import HTTPException
from moodle.proxies import proxies
from sqlalchemy.ext.asyncio import AsyncSession
from utils import validate


async def user_enrolled_courses(
		token: str,
		user: User,
		session: AsyncSession,
) -> list[WorkspaceSubjectCreate]:
	response = requests.post(
		settings.moodle.enrolled_courses_url
		% (
			url_encode(token),
			url_encode(str(user.ecourses_user_id)),
		),
		proxies=proxies,
	)
	if not isinstance(response, list):
		await validate(response.json())

	courses = []
	for course in response.json():
		if course["lastaccess"] is None:
			course["lastaccess"] = -1
		_, ids = await get_workspace_subject_ids_and_names(
			session,
			user.assigned_workspace_id,
		)
		if course["id"] not in ids:
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


async def _name_in_assignments(
		assignments: list[SubjectAssignmentCreate],
		name: str,
) -> bool:
	for assignment in assignments:
		if assignment.name == name:
			return True
	return False


async def _from_course_structure(
		token: str,
		ecourses_id: int,
		workspace_id: int,
		subject_id: int,
) -> list[SubjectAssignmentCreate] | None:
	response = requests.post(
		settings.moodle.course_structure
		% (
			url_encode(token),
			url_encode(str(ecourses_id)),
		),
		proxies=proxies,
	)
	if not isinstance(response, list):
		await validate(response.json())

	result = []
	for structure_node in response.json():
		for module in structure_node["modules"]:
			if module["modname"] == "assign":
				if await _name_in_assignments(
						result,
						module["name"],
				):
					module["name"] += f" ({structure_node["name"]})"
				result.append(
					SubjectAssignmentCreate.model_validate(
						{
							"workspace_id": workspace_id,
							"subject_id": subject_id,
							"name": module["name"],
							"url": module["url"],
						}
					)
				)
	return result


async def get_subject_assignments(
		token: str,
		subject_in: WorkspaceSubjectRead,
) -> list[SubjectAssignmentCreate] | None:
	if subject_in.ecourses_id is not None:
		return await _from_course_structure(
			token,
			subject_in.ecourses_id,
			subject_in.workspace_id,
			subject_in.id,
		)
	else:
		raise HTTPException(
			status_code=404,
			detail="Курс не найден",
		)


async def check_course_availability(
		course_id: int,
		token: str,
) -> bool:
	response = requests.post(
		settings.moodle.course_structure
		% (url_encode(token), url_encode(str(course_id))),
		proxies=proxies,
	)
	return isinstance(response.json(), list)
