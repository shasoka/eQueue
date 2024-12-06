#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.groups import GroupRead
from crud.groups import get_existing_groups, get_group
from moodle.auth import get_current_user

router = APIRouter(tags=["Groups"])


@router.get("", response_model=list[GroupRead])
async def get_groups(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    _: Annotated[User, Depends(get_current_user)],
):
    return await get_existing_groups(session)
    

@router.get("/{group_id}", response_model=GroupRead)
async def get_single_group(
    group_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    _: Annotated[User, Depends(get_current_user)],
):
    if (group := await get_group(session, group_id)) is not None:
        return group
    
    raise HTTPException(
        status_code=404,
        detail=f"Группа с id={group_id} не найдена"
    )
    
