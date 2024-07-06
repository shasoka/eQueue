from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud.users import get_all_users
from core.models import db_helper
from core.schemas.users import UserRead

router = APIRouter(
	tags=["users"],
	# responses={404: {"description": "Not found"}},
)


@router.get("", response_model=Sequence[UserRead])
async def get_users(
		session: AsyncSession = Depends(db_helper.session_getter)
):
	users = await get_all_users(session=session)
	return users
