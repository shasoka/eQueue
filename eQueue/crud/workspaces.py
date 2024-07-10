#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, Workspace, Group
from core.schemas.workspace import WorkspaceJoin, WorkspaceCreate, WorkspaceUpdate
from crud.groups import get_group
from crud.users import get_user_by_id


# noinspection PyTypeChecker
async def get_available_workspace(
    session: AsyncSession,
    user: User,
) -> Workspace | None:
    if not user.assigned_workspace_id:
        if not user.workspace_chief:
            stmt = (
                select(Workspace)
                .options(selectinload(Workspace.group).selectinload(Group.users))
                .where(Workspace.group_id == user.assigned_group_id)
            )
            result = await session.scalars(stmt)
            return result.first()
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
async def get_workspace_by_group_id(
    group_id: int,
    session: AsyncSession,
) -> Workspace | None:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.group).selectinload(Group.users))
        .where(Workspace.group_id == group_id)
    )
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_workspace_by_name(
    name: str,
    session: AsyncSession,
) -> Workspace | None:
    stmt = (
        select(Workspace)
        .options(selectinload(Workspace.group).selectinload(Group.users))
        .where(Workspace.name == name)
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


async def create_workspace(
    workspace_in: WorkspaceCreate,
    session: AsyncSession,
    user: User,
) -> Workspace | None:
    if await get_group(session, workspace_in.group_id):
        if not await get_workspace_by_group_id(workspace_in.group_id, session):
            workspace_in = workspace_in.model_dump(exclude_unset=True)
            if (
                "name" in workspace_in
                and not await get_workspace_by_name(workspace_in["name"], session)
            ) or "name" not in workspace_in:
                # Creatin new workspace via ORM model
                workspace = Workspace(**workspace_in)
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
    return None


async def update_workspace(
    workspace_upd: WorkspaceUpdate,
    session: AsyncSession,
    user: User,
) -> Workspace | None:
    if workspace := await get_workspace_by_id(
        user.assigned_workspace_id,
        session,
    ):
        workspace_upd = workspace_upd.model_dump(exclude_unset=True)
        if (
            "name" in workspace_upd
            and not await get_workspace_by_name(workspace_upd["name"], session)
        ) or "name" not in workspace_upd:
            for key, value in workspace_upd.items():
                setattr(workspace, key, value)
            await session.commit()
            await session.refresh(workspace)
            return workspace
        else:
            raise HTTPException(
                status_code=409,
                detail="Нарушено ограничение на обновление пространства",
            )
    return None


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
