#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from crud.assignments import get_submission
from crud.subjects import (
    get_workspace_subject_by_id,
    get_workspace_subject_with_assignments_by_id,
)
from crud.users import get_user_by_id


async def get_subject_queue(
    session: AsyncSession,
    user: User,
    subject_id: int,
) -> list[dict] | None:
    if subject := await get_workspace_subject_by_id(
        session,
        subject_id,
    ):
        if subject.workspace_id == user.assigned_workspace_id:
            result = []
            for user_id in subject.queue:
                cur_user = await get_user_by_id(session, user_id)
                if cur_user:
                    result.append(cur_user.dict(cast=True))
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Пользователя id={user_id} нет в очереди",
                    )
            return result
        else:
            raise HTTPException(
                status_code=403,
                detail="Вы не можете просматривать очередь в другом рабочем пространстве",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет id={subject_id} не добавлен в рабочее пространство",
        )


async def enter_subject_queue(
    session: AsyncSession,
    user: User,
    subject_id: int,
) -> list[dict] | None:
    if subject := await get_workspace_subject_by_id(
        session,
        subject_id,
    ):
        if subject.workspace_id == user.assigned_workspace_id:
            if user.id in subject.queue:
                raise HTTPException(
                    status_code=409,
                    detail="Вы уже в очереди",
                )
            else:
                result = []
                for user_id in subject.queue + [user.id]:
                    cur_user = await get_user_by_id(session, user_id)
                    if cur_user:
                        result.append(cur_user.dict(cast=True))
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Пользователя id={user_id} нет в очереди",
                        )
                subject.queue = func.array_append(subject.queue, user.id)
                await session.commit()
                return result
        else:
            raise HTTPException(
                status_code=403,
                detail="Вы не можете просматривать очередь в другом рабочем пространстве",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет id={subject_id} не добавлен в рабочее пространство",
        )


async def leave_subject_queue(
    session: AsyncSession,
    user: User,
    subject_id: int,
    mark_done: bool = False,
) -> list[dict] | None:
    if subject := await get_workspace_subject_with_assignments_by_id(
        session,
        subject_id,
    ):
        if subject.workspace_id == user.assigned_workspace_id:
            if user.id in subject.queue:
                if mark_done:
                    works = [assignment.id for assignment in subject.assignments]
                    if submission := await get_submission(
                        session,
                        user_id=user.id,
                        workspace_id=subject.workspace_id,
                        subject_id=subject_id,
                    ):
                        done = submission.submitted_works
                        next_mark = list(set(works) ^ set(done))[0]
                        submission.submitted_works = func.array_append(
                            submission.submitted_works, next_mark
                        )
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="Отсутствует submission для этого предмета",
                        )
                idx = subject.queue.index(user.id)
                result = []
                for user_id in subject.queue[:idx] + subject.queue[(idx+1):]:  # fmt: skip
                    cur_user = await get_user_by_id(session, user_id)
                    if cur_user:
                        result.append(cur_user.dict(cast=True))
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Пользователя id={user_id} нет в очереди",
                        )
                subject.queue = func.array_remove(subject.queue, user.id)
                await session.commit()
                return result
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Вы не в очереди",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail="Вы не можете просматривать очередь в другом рабочем пространстве",
            )
