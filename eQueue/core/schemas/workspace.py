#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel

from core.schemas.users import UserRead


class WorkspaceBase(BaseModel):
    group_id: int
    name: str | None
    semester: int | None
    about: str | None
    pending_users: list[int] | None


class WorkspaceRead(WorkspaceBase):
    id: int
    users: list[UserRead]


class WorkspaceReadNoSelectInLoad(WorkspaceBase):
    id: int


class WorkspaceJoin(BaseModel):
    workspace_id: int


class WorkspaceCreate(WorkspaceBase):
    group_id: int
    name: str | None = None
    semester: int | None = None
    about: str | None = None
    pending_users: list[int] | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    semester: int | None = None
    about: str | None = None
