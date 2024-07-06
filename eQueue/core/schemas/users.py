from pydantic import BaseModel


class UserMoodleLogin(BaseModel):
	login: str
	password: str
	group_id: int


class UserBase(BaseModel):
	moodle_token: str
	ecourses_user_id: int
	assigned_group_id: int
	first_name: str
	second_name: str
	status: str
	talon: str
	user_picture_url: str


class UserCreate(UserBase):
	pass


class UserRead(UserBase):
	id: int
	created_at: str
