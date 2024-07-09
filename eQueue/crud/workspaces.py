#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, Workspace, Group
from core.schemas.workspace import WorkspaceJoin, WorkspaceCreate, WorkspaceUpdate
from crud.groups import get_group


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


async def create_workspace(
    workspace_in: WorkspaceCreate,
    session: AsyncSession,
) -> Workspace | None:
    if await get_group(session, workspace_in.group_id):
        if not await get_workspace_by_group_id(workspace_in.group_id, session):
            workspace_in = workspace_in.model_dump(exclude_unset=True)
            if (
                "name" in workspace_in
                and not await get_workspace_by_name(workspace_in["name"], session)
            ) or "name" not in workspace_in:
                workspace = Workspace(**workspace_in)
                session.add(workspace)
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
    return None


async def update_pending_users(
    session: AsyncSession,
    workspace_upd: WorkspaceJoin,
    user: User,
) -> Workspace | None:
    if (
        workspace := await get_workspace_by_id(workspace_upd.workspace_id, session)
    ) is not None:
        if user.id not in workspace.pending_users:
            workspace.pending_users = func.array_append(
                workspace.pending_users, user.id
            )
            await session.commit()
            await session.refresh(workspace)
            return workspace
    return None
