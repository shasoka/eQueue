from pydantic import BaseModel

from core.schemas.users import UserRead


class GroupBase(BaseModel):
    id: int
    name: str


class GroupRead(GroupBase):
    users: list[UserRead]
