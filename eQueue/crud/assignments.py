#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models.entities import SubjectAssignment
from core.schemas.subjects import WorkspaceSubjectRead
from crud.workspaces import get_workspace_subjects_casted
from moodle.courses import get_subject_assignments


async def generate_subject_assignment(
    session: AsyncSession,
    user: User,
    subject_in: WorkspaceSubjectRead,
) -> list[SubjectAssignment] | None:
    if subject_in.workspace_id == user.assigned_workspace_id:
        if existing_subjects := await get_workspace_subjects_casted(
            session=session,
            workspace_id=subject_in.workspace_id,
        ):
            if (
                WorkspaceSubjectRead.model_validate(subject_in.model_dump())
                in existing_subjects
            ):
                result = []
                available_assignments = await get_subject_assignments(
                    token=user.access_token,
                    subject_in=subject_in,
                )
                for assignment in available_assignments:
                    new_assign = SubjectAssignment(**assignment.model_dump())
                    try:
                        session.add(new_assign)
                        await session.flush()
                    except IntegrityError as e:
                        raise HTTPException(
                            status_code=409,
                            detail=f"Нарушено ограничение уникальносьти. Работа '{new_assign.name}' уже добавлена",
                        )
                    result.append(new_assign)
                await session.commit()
                return result
            else:
                raise HTTPException(
                    status_code=403,
                    detail=f"Предмета id={subject_in.ecourses_id} нет в пространстве {subject_in.workspace_id}",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail=f"В пространстве {subject_in.workspace_id} нет ни одного предмета",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Вы не можете добавлять предметы в рабочее пространство {subject_in.workspace_id}",
        )
