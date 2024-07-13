#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, Workspace, Group, WorkspaceSubject, UserSubmission
from core.models.entities import SubjectAssignment
from core.schemas.subjects import WorkspaceSubjectRead
from core.schemas.workspace import WorkspaceJoin, WorkspaceCreate, WorkspaceUpdate
from crud.groups import get_group
from crud.users import get_user_by_id


# noinspection PyTypeChecker
async def get_assignments_count_for_subject(
    session: AsyncSession,
    subject_id: int,
) -> int:
    stmt = (
        select(func.count())
        .select_from(SubjectAssignment)
        .where(SubjectAssignment.subject_id == subject_id)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_available_workspace(
    session: AsyncSession,
    user: User,
) -> list[Workspace] | None:
    if not user.assigned_workspace_id:
        if not user.workspace_chief:
            stmt = (
                select(Workspace)
                .options(selectinload(Workspace.group).selectinload(Group.users))
                .where(Workspace.group_id == user.assigned_group_id)
            )
            result = await session.scalars(stmt)
            return list(result.all())
    return None


# noinspection PyTypeChecker
async def get_workspace_by_id(
    workspace_id: int,
    session: AsyncSession,
) -> Workspace | None:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.group).selectinload(Group.users))
        .where(Workspace.id == workspace_id)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_by_constraint(
    group_id: int,
    name: str,
    session: AsyncSession,
) -> Workspace | None:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.group).selectinload(Group.users))
        .where(Workspace.group_id == group_id)
        .where(Workspace.name == name)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def check_workspace_constraint(
    name: str,
    group_id: int,
    session: AsyncSession,
) -> Workspace | None:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.group).selectinload(Group.users))
        .where(Workspace.name == name)
        .where(Workspace.group_id == group_id)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_with_assignees(
    session: AsyncSession,
    group_id: int,
) -> Workspace | None:
    stmt = (select(Workspace).options(selectinload(Workspace.users))).where(
        Workspace.group_id == group_id
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_subject_ids_and_names(
    session: AsyncSession,
    workspace_id: int,
    ecourse_id: bool = True,
) -> tuple[list[str], list[int | None]]:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.subjects))
        .where(Workspace.id == workspace_id)
    )
    result = await session.scalars(stmt)
    workspace = result.first()
    if workspace:
        if ecourse_id:
            return (
                [subj.name for subj in workspace.subjects],
                [subj.ecourses_id for subj in workspace.subjects],
            )
        else:
            return (
                [subj.name for subj in workspace.subjects],
                [subj.id for subj in workspace.subjects],
            )
    else:
        return [], []


# noinspection PyTypeChecker
async def get_workspace_subjects_casted(
    session: AsyncSession,
    workspace_id: int,
) -> list[WorkspaceSubjectRead]:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.subjects))
        .where(Workspace.id == workspace_id)
    )
    result = await session.scalars(stmt)
    workspace = result.first()
    return [
        WorkspaceSubjectRead.model_validate(subj.dict()) for subj in workspace.subjects
    ]


# noinspection PyTypeChecker
async def get_workspace_subjects(
    session: AsyncSession,
    workspace_id: int,
) -> list[WorkspaceSubject]:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.subjects))
        .where(Workspace.id == workspace_id)
    )
    result = await session.scalars(stmt)
    workspace = result.first()
    return workspace.subjects


async def create_workspace(
    workspace_in: WorkspaceCreate,
    session: AsyncSession,
    user: User,
) -> Workspace | None:
    if await get_group(session, workspace_in.group_id):
        if not await get_workspace_by_constraint(
            workspace_in.group_id,
            workspace_in.name,
            session,
        ):
            # Creating new workspace via ORM model
            workspace = Workspace(**workspace_in.model_dump(exclude_unset=True))
            session.add(workspace)
            await session.flush()  # Getting new workspace id

            # Updating user
            user.workspace_chief = True
            user.assigned_workspace_id = workspace.id
            await session.flush()

            # Commit and refresh objects to return
            await session.commit()
            await session.refresh(workspace)

            return workspace
        else:
            raise HTTPException(
                status_code=409,
                detail="Нарушено ограничение на создание пространства",
            )
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Не нашлось группы с id={workspace_in.group_id}",
        )


async def update_workspace(
    workspace_upd: WorkspaceUpdate,
    session: AsyncSession,
    user: User,
) -> Workspace | None:
    if workspace := await get_workspace_by_id(
        user.assigned_workspace_id,
        session,
    ):
        if not await check_workspace_constraint(
            workspace_upd.name,
            user.assigned_group_id,
            session,
        ):
            for key, value in workspace_upd.model_dump(exclude_unset=True).items():
                setattr(workspace, key, value)
            await session.commit()
            await session.refresh(workspace)
            return workspace
        else:
            raise HTTPException(
                status_code=409,
                detail="Нарушено ограничение на обновление пространства",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail="Не найдено ни одного рабочего пространства",
        )


async def update_pending_users(
    session: AsyncSession,
    workspace_upd: WorkspaceJoin,
    user: User,
) -> Workspace | None:
    if workspace := (
        await get_workspace_by_id(
            workspace_upd.workspace_id,
            session,
        )
    ):
        if user.assigned_group_id == workspace.group_id:
            if user.id not in workspace.pending_users:
                workspace.pending_users = func.array_append(
                    workspace.pending_users, user.id
                )
                await session.commit()
                await session.refresh(workspace)
                return workspace
            else:
                raise HTTPException(
                    status_code=409,
                    detail="Пользователь уже подал заявку на вступление в рабочее пространство",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail="Вы не можете подать заявку на вступление в рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail="Не найдено ни одно рабочее пространство",
        )


async def accept_pending(
    user_id: int,
    session: AsyncSession,
    user: User,
) -> User | None:
    if joining_user := await get_user_by_id(session, user_id):
        if workspace := await get_workspace_by_id(
            user.assigned_workspace_id,
            session,
        ):
            if joining_user.assigned_group_id == workspace.group_id:
                if user_id in workspace.pending_users:
                    workspace.pending_users = func.array_remove(
                        workspace.pending_users, user_id
                    )
                    joining_user.assigned_workspace_id = workspace.id
                    for subject in await get_workspace_subjects(
                        session,
                        workspace.id,
                    ):
                        session.add(
                            UserSubmission(
                                user_id=joining_user.id,
                                workspace_id=workspace.id,
                                subject_id=subject.id,
                                total_required_works=await get_assignments_count_for_subject(
                                    session,
                                    subject.id,
                                ),
                            )
                        )
                    await session.commit()
                    await session.refresh(workspace)
                    await session.refresh(joining_user)
                    return joining_user
                else:
                    raise HTTPException(
                        status_code=409,
                        detail="Пользователь не подал заявку на вступление в рабочее пространство",
                    )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Пользователь прикреплен к группе отличной от группы рабочего пространства",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Не найдено ни одно рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail="Не найден пользователь с таким id",
        )


# noinspection PyTypeChecker
async def clear_assignments_on_user_leave(
    session: AsyncSession,
    user_id: int,
):
    stmt = delete(UserSubmission).where(UserSubmission.user_id == user_id)
    await session.execute(stmt)


async def leave_workspace(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    if user := await get_user_by_id(session, user_id):
        if workspace := await get_workspace_with_assignees(
            session, user.assigned_group_id
        ):
            if user in workspace.users:
                if len(workspace.users) == 1:
                    user.assigned_workspace_id = None
                    user.workspace_chief = False
                    await session.delete(workspace)
                    await session.commit()
                    await session.refresh(user)
                    return user
                if not user.workspace_chief:
                    user.assigned_workspace_id = None
                    await clear_assignments_on_user_leave(session, user_id)
                    await session.commit()
                    await session.refresh(user)
                    return user
                else:
                    raise HTTPException(
                        # Precondition required
                        status_code=428,
                        detail="Вы явялетесь администратором рабочего пространства. "
                        "Сперва передайте права другому пользователю",
                    )
            else:
                raise HTTPException(
                    status_code=409,
                    detail="Вы не прикреплены ни к одному рабочему пространству",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Не найдено ни одно рабочее пространство",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail="Не найден пользователь с таким id",
        )


async def workspace_safe_delete(session: AsyncSession, user: User) -> Workspace | None:
    if workspace := await get_workspace_with_assignees(
        session=session, group_id=user.assigned_group_id
    ):
        for user in workspace.users:
            user.assigned_workspace_id = None
            user.workspace_chief = False
        await session.delete(workspace)
        await session.commit()
        return workspace
    raise HTTPException(
        status_code=404,
        detail="Не найдено ни одно рабочее пространство",
    )


async def raise_user(
    session: AsyncSession,
    user_id: int,
    user: User,
) -> User | None:
    # если айди равны, то нахуй
    # если айди разные проверить что юзер админ или нет
    # если айди разные проверить что юзер с юзер_айди есть в воркспейсе
    if not user.id == user_id:
        if user.workspace_chief:
            if inheritor := await get_user_by_id(session, user_id):
                if workspace := await get_workspace_with_assignees(
                    session, user.assigned_group_id
                ):
                    if inheritor in workspace.users:
                        inheritor.workspace_chief = True
                        user.workspace_chief = False
                        await session.commit()
                        await session.refresh(inheritor)
                        return inheritor
                    else:
                        raise HTTPException(
                            status_code=409,
                            detail="Пользователь не прикреплен к рабочему пространству",
                        )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Не найдено ни одно рабочее пространство",
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Не найден пользователь с таким id",
                )
        else:
            raise HTTPException(
                status_code=403,
                detail="Вы не являетесь руководителем рабочего пространства",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Вы уже являетесь руководителем рабочего пространства",
        )
