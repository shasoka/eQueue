from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.users import UserCreate


async def get_user_by_token(
		session: AsyncSession,
		access_token: str
) -> User | None:
	# TODO: make with get
	stmt = select(User).where(User.access_token == access_token)
	result = await session.scalars(stmt)
	return result.first()


async def get_user_by_ecourses_id(
		session: AsyncSession,
		ecourses_user_id: int
) -> User | None:
	# TODO: make with get
	stmt = select(User).where(User.ecourses_user_id == ecourses_user_id)
	result = await session.scalars(stmt)
	return result.first()


async def get_all_users(session: AsyncSession) -> Sequence[User]:
	stmt = select(User).order_by(User.id)
	result = await session.scalars(stmt)
	return result.all()


async def create_new_user(
		session: AsyncSession,
		user_in: UserCreate
) -> User:
	user = User(**user_in.model_dump())
	session.add(user)
	await session.commit()
	return user
