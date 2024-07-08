import datetime

from fastapi import Form
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from core.schemas.moodle import MoodleTokenMixin


class UserBase(BaseModel):
	ecourses_user_id: int
	assigned_group_id: int | None = None
	first_name: str
	second_name: str
	status: str | None = None
	talon: str
	user_picture_url: str


class UserRead(UserBase):
	id: int
	created_at: datetime.datetime


class UserAuth(UserRead, MoodleTokenMixin):
	token_type: str = "Bearer"


class UserCreate(UserBase, MoodleTokenMixin):
	pass


class UserUpdate(UserBase, MoodleTokenMixin):
	access_token: str | None = None
	ecourses_user_id: int | None = None
	assigned_group_id: int | None = None
	first_name: str | None = None
	second_name: str | None = None
	status: str | None = None
	talon: str | None = None
	user_picture_url: str | None = None
