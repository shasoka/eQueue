#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.subject_assignments import (
    SubjectAssignmentRead,
    SubjectAssignmentCreate,
    SubjectAssignmentUpdate,
)
from core.schemas.subjects import (
    WorkspaceSubjectCreate,
    WorkspaceSubjectRead,
    WorkspaceSubjectUpdate,
)
from core.schemas.user_submissions import UserSubmissionRead, UserSubmissionUpdate
from crud.assignments import (
    generate_subject_assignment,
    add_assignment,
    update_submission_submitted_works,
    partial_update_assignment,
    delete_workspace_subject_assignment,
)
from crud.subjects import (
    create_workspace_subject,
    partial_update_workspace_subject,
    delete_workspace_subject,
)
from moodle.auth import get_current_user
from moodle.courses import user_enrolled_courses

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
    "",
    response_model=list[WorkspaceSubjectRead],
)
async def add_subjects(
    user_selection: list[WorkspaceSubjectCreate],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    if not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете добавлять предметы, т.к. вы не являетесь руководителем рабочего пространства",
        )
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


@router.patch(
    "",
    response_model=WorkspaceSubjectRead,
)
async def update_subject(
    subject_in: WorkspaceSubjectUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await partial_update_workspace_subject(
        session=session,
        user=current_user,
        subject_in=subject_in,
    )


@router.post(
    settings.api.v1.gen_subject_assignments,
    response_model=list[SubjectAssignmentRead],
)
async def generate_assignments_from_ecourses(
    user_selection: list[WorkspaceSubjectRead],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    if not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете добавлять предметы, т.к. вы не являетесь руководителем рабочего пространства",
        )
    resposne = []
    for course in user_selection:
        resposne.extend(
            await generate_subject_assignment(
                session=session,
                user=current_user,
                subject_in=course,
            )
        )
    return resposne


@router.post(
    settings.api.v1.add_subject_assignments,
    response_model=SubjectAssignmentRead,
)
async def add_assignment_manually(
    assignnment_in: SubjectAssignmentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    if not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете добавлять предметы, т.к. вы не являетесь руководителем рабочего пространства",
        )
    return await add_assignment(
        session=session,
        user=current_user,
        assignment_in=assignnment_in,
    )


@router.patch(
    settings.api.v1.update_subject_assignments,
    response_model=SubjectAssignmentRead,
)
async def update_assignment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    assignment_in: SubjectAssignmentUpdate,
):
    return await partial_update_assignment(
        session=session,
        assignment_in=assignment_in,
        user=current_user,
    )


@router.patch(
    settings.api.v1.mark_assignment,
    response_model=UserSubmissionRead,
)
async def update_user_submitted_works(
    submission_in: UserSubmissionUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await update_submission_submitted_works(
        session=session,
        user=current_user,
        submission_in=submission_in,
    )


@router.delete(
    settings.api.v1.delete_subject_assignment,
    response_model=SubjectAssignmentRead,
)
async def delete_assignment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    assignment_id: int,
):
    return await delete_workspace_subject_assignment(
        session=session,
        user=current_user,
        assignment_id=assignment_id,
    )


@router.delete(
    "/{subject_id}",
    response_model=WorkspaceSubjectRead,
)
async def delete_subject(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    subject_id: int,
):
    return await delete_workspace_subject(
        session=session,
        user=current_user,
        subject_id=subject_id,
    )
