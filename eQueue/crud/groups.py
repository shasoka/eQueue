#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Group


async def get_group(session: AsyncSession, group_id: int) -> Group | None:
    return await session.get(Group, group_id)


# noinspection PyTypeChecker
async def get_existing_groups(session: AsyncSession) -> list[Group]:
    groups = await session.execute(select(Group).options(selectinload(Group.users)))
    return groups.scalars().all()
