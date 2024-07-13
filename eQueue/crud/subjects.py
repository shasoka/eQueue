#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import WorkspaceSubject, User
from core.schemas.subjects import WorkspaceSubjectCreate, WorkspaceSubjectUpdate
from crud.assignments import add_submission
from crud.users import get_user_by_id
from crud.workspaces import (
    get_workspace_subject_ids_and_names,
)
from moodle.courses import check_course_availability


# noinspection PyTypeChecker
async def get_workspace_subject_by_id(
    session: AsyncSession,
    subject_id: int,
) -> WorkspaceSubject | None:
    stmt = select(WorkspaceSubject).where(WorkspaceSubject.id == subject_id)
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_subject_with_assignments_by_id(
    session: AsyncSession,
    subject_id: int,
) -> WorkspaceSubject | None:
    stmt = (
        select(WorkspaceSubject)
        .where(WorkspaceSubject.id == subject_id)
        .options(selectinload(WorkspaceSubject.assignments))
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_subject_names_by_id(
    session: AsyncSession,
) -> WorkspaceSubject | None:
    stmt = select(WorkspaceSubject)
    result = await session.scalars(stmt)
    subjects = result.all()
    if subjects:
        return [subject.name for subject in subjects]
    return None


async def create_workspace_subject(
    session: AsyncSession,
    user: User,
    subject_in: WorkspaceSubjectCreate,
) -> WorkspaceSubject | None:
    if subject_in.workspace_id == user.assigned_workspace_id:
        if subject_in.ecourses_id:
            if not await check_course_availability(
                course_id=subject_in.ecourses_id,
                token=user.access_token,
            ):
                raise HTTPException(
                    status_code=403,
                    detail=f"Вы не имеете доступа к предмету {subject_in.ecourses_id}",
                )
        names, ids = await get_workspace_subject_ids_and_names(
            session,
            user.assigned_workspace_id,
        )
        if (subject_in.ecourses_id not in ids) and (subject_in.name not in names):
            subject = WorkspaceSubject(**subject_in.model_dump())
            session.add(subject)
            await session.flush()
            await add_submission(
                session=session,
                group_id=user.assigned_group_id,
                subject_id=subject.id,
            )
            await session.commit()
            await session.refresh(subject)
            return subject
        else:
            raise HTTPException(
                status_code=409,
                detail=f"Предмет уже добавлен в рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Вы не можете добавлять предметы в рабочее пространство {subject_in.workspace_id}",
        )


async def partial_update_workspace_subject(
    session: AsyncSession,
    user: User,
    subject_in: WorkspaceSubjectUpdate,
) -> WorkspaceSubject | None:
    if subject_in.workspace_id == user.assigned_workspace_id:
        if subject := await get_workspace_subject_by_id(
            session=session,
            subject_id=subject_in.id,
        ):
            subject_in = subject_in.model_dump(exclude_unset=True)
            for key, value in subject_in.items():
                setattr(subject, key, value)
            try:
                await session.commit()
                await session.refresh(subject)
                return subject
            except IntegrityError:
                raise HTTPException(
                    status_code=409,
                    detail=f"Предмет {subject_in["name"]} уже добавлен в рабочее пространство",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Предмет id={subject_in.id} не добавлен в рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Вы не можете добавлять предметы в рабочее пространство {subject_in.workspace_id}",
        )


async def delete_workspace_subject(
    session: AsyncSession,
    user: User,
    subject_id: int,
) -> WorkspaceSubject:
    if user.workspace_chief:
        if subject := await get_workspace_subject_by_id(
            session=session,
            subject_id=subject_id,
        ):
            if subject.workspace_id == user.assigned_workspace_id:
                await session.delete(subject)
                await session.commit()
                return subject
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Вы не можете удалять предметы в другом рабочем пространстве",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Предмет id={subject_id} не добавлен в рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Вы не являетесь администратором рабочего пространства",
        )
