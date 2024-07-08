import datetime

from fastapi import Form
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from core.schemas.moodle import MoodleTokenMixin


@dataclass
class AdditionalLoginFormFields:
	group_id: int = Form()


class UserBase(BaseModel):
	ecourses_user_id: int
	assigned_group_id: int | None = None
	first_name: str
	second_name: str
	status: str | None = None
	talon: str
	user_picture_url: str


class UserCreate(UserBase, MoodleTokenMixin):
	pass


class UserRead(UserBase):
	id: int
	created_at: datetime.datetime


class UserAuth(UserRead, MoodleTokenMixin):
	token_type: str = "Bearer"
