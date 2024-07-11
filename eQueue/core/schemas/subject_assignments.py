#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel


class SubjectAssignmentBase(BaseModel):
    workspace_id: int
    subject_id: int
    name: str
    url: str | None


class SubjectAssignmentRead(SubjectAssignmentBase):
    id: int


class SubjectAssignmentCreate(SubjectAssignmentBase):
    url: str | None = None
