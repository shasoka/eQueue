#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from core.config import settings
from core.models import db_helper, User
from core.schemas.moodle import MoodleLogin
from core.schemas.users import UserRead, UserCreate, UserAuth, UserUpdate
from core.schemas.workspace import (
    WorkspaceBase,
    WorkspaceRead,
    WorkspaceJoin,
    WorkspaceCreate,
    WorkspaceReadNoSelectInLoad,
    WorkspaceUpdate,
)
from crud.users import create_new_user, get_user_by_ecourses_id, update_user
from crud.workspaces import (
    get_available_workspace,
    update_pending_users,
    create_workspace,
    update_workspace,
)
from moodle.auth import (
    auth_by_moodle_credentials,
    get_moodle_user_info,
    token_persistence,
    get_current_user,
)
from moodle.users import patch_profile_picture

router = APIRouter(
    tags=["Workspaces"],
)


@router.get("", response_model=WorkspaceRead)
async def get_workspace(
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


@router.patch("/join", response_model=WorkspaceRead)
async def join_workspace(
    workspace_upd: WorkspaceJoin,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if workspace := await update_pending_users(
        session=session,
        workspace_upd=workspace_upd,
        user=current_user,
    ):
        return workspace
    raise HTTPException(
        status_code=404,
        detail="Не найдено ни одно рабочее пространство или пользователь уже подал заявку на вступление в группу",
    )


# TODO: Удаление пространства (учесть зависимости от воркспейса)
# TODO: выход из пространства (учесть что чел может быть шефом)
# TODO: accept users from pending
