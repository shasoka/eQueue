from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.moodle import MoodleLogin
from core.schemas.users import UserRead, UserCreate, UserAuth, UserUpdate
from crud.users import create_new_user, get_user_by_ecourses_id, update_user
from moodle.auth import auth_by_moodle_credentials, get_moodle_user_info, token_persistence, get_current_user
from moodle.users import patch_profile_picture

router = APIRouter(
	tags=["users"],
	# responses={404: {"description": "Not found"}},  # TODO
)


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
		user = await update_user(
			session=session,
			user=user,
			user_upd=UserUpdate(
				access_token=token,
			)
		)
	# Returns user with token and token_type
	user = UserAuth.model_validate(user.dict()).model_dump()
	return user


@router.head(settings.api.v1.token_persistence)
async def check_token_persistence(
		current_user: Annotated[User, Depends(get_current_user)]
):
	try:
		await token_persistence(current_user.access_token)
		return Response(status_code=200, headers={"Token-Alive": "true"})
	except HTTPException:
		return Response(status_code=401, headers={"Token-Alive": "false"})


@router.get("", response_model=UserRead)
async def get_user(
		current_user: Annotated[User, Depends(get_current_user)]
):
	return current_user


@router.patch("", response_model=UserRead)
async def partial_update_user(
		user_upd: UserUpdate,
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
		current_user: Annotated[User, Depends(get_current_user)]
):
	return await update_user(
		session=session,
		user=current_user,
		user_upd=user_upd
	)


@router.patch("/change_profile_picture")
async def upload_avatar(
		file: Annotated[UploadFile, File(...)],
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
		current_user: Annotated[User, Depends(get_current_user)]
):
	return await update_user(
		session=session,
		user=current_user,
		user_upd=UserUpdate(
			user_picture_url=await patch_profile_picture(
				token=current_user.access_token,
				files={'filedata': (file.filename, file.file, file.content_type)}
			)
		)
	)
