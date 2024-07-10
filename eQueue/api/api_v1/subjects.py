#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.moodle import (
    MoodleLogin,
    EcoursesSubjectDescription,
    EcoursesSubjectStructure,
)
from core.schemas.users import UserRead, UserCreate, UserAuth, UserUpdate
from crud.users import create_new_user, get_user_by_ecourses_id, update_user
from moodle.auth import (
    auth_by_moodle_credentials,
    get_moodle_user_info,
    token_persistence,
    get_current_user,
)
from moodle.courses import user_enrolled_courses
from moodle.courses.requests import get_course_data
from moodle.users import patch_profile_picture

router = APIRouter(
    tags=["Subjects"],
)


@router.get(
    settings.api.v1.ecourses_enrolled, response_model=list[EcoursesSubjectDescription]
)
async def get_courses_from_moodle(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await user_enrolled_courses(
        token=current_user.access_token,
        ecourses_user_id=current_user.ecourses_user_id,
    )


@router.post("/tst", response_model=EcoursesSubjectStructure)
async def test(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_course_data(
        course_id=9882,
        token=current_user.access_token,
    )
