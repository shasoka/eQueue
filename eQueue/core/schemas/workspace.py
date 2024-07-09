from pydantic import BaseModel

from core.schemas.groups import GroupRead


class WorkspaceBase(BaseModel):
    name: str | None
    semester: int | None
    about: str | None
    pending_users: list[int] | None


class WorkspaceRead(WorkspaceBase):
    id: int
    group: GroupRead


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
