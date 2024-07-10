#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
#
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Group


async def get_group(session: AsyncSession, group_id: int) -> Group | None:
    return await session.get(Group, group_id)
