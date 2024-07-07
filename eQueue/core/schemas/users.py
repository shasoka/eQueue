import datetime

from pydantic import BaseModel

from core.schemas.moodle import MoodleLogin


class UserMoodleLogin(MoodleLogin):
	group_id: int


class UserBase(BaseModel):
	moodle_token: str
	ecourses_user_id: int
	assigned_group_id: int
	first_name: str
	second_name: str
	status: str | None = None
	talon: str
	user_picture_url: str


class UserCreate(UserBase):
	pass


class UserRead(UserBase):
	id: int
	created_at: datetime.datetime
