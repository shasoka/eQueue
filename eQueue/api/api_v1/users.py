from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.moodle import MoodleLogin
from core.schemas.users import UserRead, UserCreate, UserAuth
from crud.users import get_all_users, create_new_user, get_user_by_ecourses_id
from moodle.auth import auth_by_moodle_credentials, get_moodle_user_info, token_persistence, get_current_user

router = APIRouter(
	tags=["users"],
	# responses={404: {"description": "Not found"}},  # TODO
)


@router.head(settings.api.v1.token_persistence, response_model=UserRead)
async def check_token_persistence():
	await token_persistence()
	# TODO: implement
	return Response(status_code=200)


@router.get("", response_model=Sequence[UserRead])
async def get_users(
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
		current_user: Annotated[User, Depends(get_current_user)]
):
	users = await get_all_users(session=session)
	return users


@router.post(settings.api.v1.moodle_auth, response_model=UserAuth)
async def login_user(
		credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
	# 1. Try to auth user through e.sfu-kras.ru/login
	token = await auth_by_moodle_credentials(
		MoodleLogin(
			login=credentials.username,
			password=credentials.password
		)
	)
	# 2. On success auth get user info
	user_info = await get_moodle_user_info(
		token=token,
	)
	# 3. Check if user registered in eQueue
	if not (
			user := await get_user_by_ecourses_id(
				session=session,
				ecourses_user_id=user_info["ecourses_user_id"]
			)
	):
		# User is not registered
		user = await create_new_user(
			session=session,
			user_in=UserCreate(**user_info)
		)
	else:
		# User is registered
		# TODO: Update user token
		pass
	# Returns user with token and token_type
	user = UserAuth.model_validate(user.dict()).model_dump()
	return user


@router.patch("", response_model=UserRead)
async def refresh_user_ecourses_data():
	raise NotImplementedError  # TODO
