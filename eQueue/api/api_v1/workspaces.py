from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.moodle import MoodleLogin
from core.schemas.users import UserRead, UserCreate, UserAuth, UserUpdate
from core.schemas.workspace import WorkspaceBase
from crud.users import create_new_user, get_user_by_ecourses_id, update_user
from crud.workspaces import get_workspace_by_group_id
from moodle.auth import auth_by_moodle_credentials, get_moodle_user_info, token_persistence, get_current_user
from moodle.users import patch_profile_picture

router = APIRouter(
	tags=["Workspaces"],
)


@router.get("")
async def get_workspaces(
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
		current_user: Annotated[User, Depends(get_current_user)]
):
	return await get_workspace_by_group_id(
		session=session,
		current_user=current_user
	)
