#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
#
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
    SelectedCourses,
)
from core.schemas.subjects import WorkspaceSubjectCreate, WorkspaceSubjectRead
from core.schemas.users import UserRead, UserCreate, UserAuth, UserUpdate
from crud.subjects import create_workspace_subject
from crud.users import create_new_user, get_user_by_ecourses_id, update_user
from moodle.auth import (
    auth_by_moodle_credentials,
    get_moodle_user_info,
    token_persistence,
    get_current_user,
)
from moodle.courses import user_enrolled_courses
from moodle.users import patch_profile_picture

router = APIRouter(
    tags=["Subjects"],
)


@router.get(
    settings.api.v1.ecourses_enrolled,
    response_model=list[WorkspaceSubjectCreate],
)
async def get_courses_from_moodle(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await user_enrolled_courses(
        token=current_user.access_token,
        user=current_user,
        session=session,
    )


@router.post(
    settings.api.v1.fill_workspace_ecourses,
    response_model=list[WorkspaceSubjectRead],
)
async def fill_workspace_with_ecourses(
    user_selection: list[WorkspaceSubjectCreate] | list[int],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    resposne = []
    for course in user_selection:
        resposne.append(
            await create_workspace_subject(
                session=session,
                user=current_user,
                subject_in=course,
            )
        )
    return resposne
