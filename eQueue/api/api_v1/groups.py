#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.groups import GroupRead
from crud.groups import get_existing_groups
from moodle.auth import get_current_user

router = APIRouter(tags=["Groups"])


@router.get("", response_model=list[GroupRead])
async def get_groups(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    _: Annotated[User, Depends(get_current_user)],
):
    return await get_existing_groups(session)
