#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Group
from core.schemas.users import UserCreate, UserUpdate


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


# noinspection PyTypeChecker
async def get_user_by_token(session: AsyncSession, access_token: str) -> User | None:
    stmt = select(User).where(User.access_token == access_token)
    result = await session.scalars(stmt)
    return result.first()


# noinspection PyTypeChecker
async def get_user_by_ecourses_id(
    session: AsyncSession, ecourses_user_id: int
) -> User | None:
    stmt = select(User).where(User.ecourses_user_id == ecourses_user_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_new_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_upd: UserUpdate,
) -> User:
    user_upd = user_upd.model_dump(exclude_unset=True)
    if "assigned_group_id" in user_upd:
        if await session.get(Group, user_upd["assigned_group_id"]) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Группа id={user_upd['assigned_group_id']} не существует",
            )
    for key, value in user_upd.items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
