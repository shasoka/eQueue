#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.users import UserRead
from core.schemas.workspace import (
    WorkspaceRead,
    WorkspaceJoin,
    WorkspaceCreate,
    WorkspaceReadNoSelectInLoad,
    WorkspaceUpdate,
)
from crud.workspaces import (
    get_available_workspace,
    update_pending_users,
    create_workspace,
    update_workspace,
    accept_pending,
    leave_workspace,
    workspace_safe_delete,
    raise_user,
)
from moodle.auth import (
    get_current_user,
)

router = APIRouter(
    tags=["Workspaces"],
)


@router.get("", response_model=list[WorkspaceRead])
async def get_exisiting_workspace(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if workspace := await get_available_workspace(session=session, user=current_user):
        return workspace
    raise HTTPException(404, detail="Не найдено ни одно рабочее пространство")


@router.post("", response_model=WorkspaceReadNoSelectInLoad)
async def create_new_workspace(
    workspace_in: WorkspaceCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.assigned_group_id != workspace_in.group_id:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете создать рабочее пространство в этой группе",
        )
    if workspace := await create_workspace(
        workspace_in=workspace_in, session=session, user=current_user
    ):
        return workspace
    raise HTTPException(
        409, detail="Нарушено ограничение на создание рабочего пространства"
    )


@router.patch("", response_model=WorkspaceReadNoSelectInLoad)
async def update_workspace_data(
    workspace_upd: WorkspaceUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.assigned_workspace_id or not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете обновить данные рабочего пространства",
        )
    if workspace := await update_workspace(
        workspace_upd=workspace_upd,
        session=session,
        user=current_user,
    ):
        return workspace
    raise HTTPException(
        status_code=404,
        detail="Не найдено ни одно рабочее пространство или пользователь уже подал заявку на вступление в группу",
    )


@router.patch(settings.api.v1.join_workspace, response_model=WorkspaceRead)
async def join_workspace(
    workspace_upd: WorkspaceJoin,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await update_pending_users(
        session=session,
        workspace_upd=workspace_upd,
        user=current_user,
    )


@router.patch(settings.api.v1.raise_user, response_model=UserRead)
async def make_user_workspace_chief(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await raise_user(session=session, user=current_user, user_id=user_id)


@router.post(settings.api.v1.accept_pending, response_model=UserRead)
async def accept_join_request(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете подтвердить заявку на вступление в рабочее пространство",
        )
    return await accept_pending(
        user_id=user_id,
        session=session,
        user=current_user,
    )


@router.post(settings.api.v1.leave_workspace, response_model=UserRead)
async def user_leave_workspace(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.id != user_id and not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете исключать других участников рабочего пространства",
        )
    return await leave_workspace(
        user_id=user_id,
        session=session,
    )


@router.delete("", response_model=WorkspaceReadNoSelectInLoad)
async def delete_workspace(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.assigned_workspace_id or not current_user.workspace_chief:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете удалить рабочее пространство",
        )
    return await workspace_safe_delete(
        session=session,
        user=current_user,
    )
