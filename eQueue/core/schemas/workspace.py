from pydantic import BaseModel

from core.schemas.users import UserRead


class WorkspaceBase(BaseModel):
	semester: int
	chief: UserRead
