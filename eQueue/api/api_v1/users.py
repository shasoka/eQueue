from typing import Sequence, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.users import UserRead, UserMoodleLogin, UserCreate
from crud.users import get_all_users, create_new_user
from moodle.auth import auth_by_moodle_credentials, get_moodle_user_info

router = APIRouter(
	tags=["users"],
	# responses={404: {"description": "Not found"}},
)


@router.get("", response_model=Sequence[UserRead])
async def get_users(
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
	users = await get_all_users(session=session)
	return users


@router.post("", response_model=UserRead)
async def create_user(
		user_in: UserMoodleLogin,
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
	# 1. Try to auth user through e.sfu-kras.ru/login
	token = await auth_by_moodle_credentials(user_in)
	# 2. On success auth get user info
	user_info = await get_moodle_user_info(
		token=token,
		group_id=user_in.group_id
	)
	# 3. Create new user
	user = await create_new_user(
		session=session,
		user_in=UserCreate(**user_info)
	)
	return user


@router.patch("", response_model=UserRead)
async def refresh_user_ecourses_data():
	raise NotImplementedError  # TODO
