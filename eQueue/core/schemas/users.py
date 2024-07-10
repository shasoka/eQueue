#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

import datetime

from pydantic import BaseModel

from core.schemas.moodle import MoodleTokenMixin


class UserBase(BaseModel):
    ecourses_user_id: int
    assigned_group_id: int | None = None
    assigned_workspace_id: int | None = None
    workspace_chief: bool = False
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
    assigned_workspace_id: int | None = None
    workspace_chief: bool = False
    first_name: str | None = None
    second_name: str | None = None
    status: str | None = None
    talon: str | None = None
    user_picture_url: str | None = None
