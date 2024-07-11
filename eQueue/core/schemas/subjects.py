#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel


class WorkspaceSubjectBase(BaseModel):
    workspace_id: int
    ecourses_id: int | None
    name: str
    ecourses_link: str | None
    professor: str | None
    professor_contact: str | None
    requirements: str | None
    additional_fields: dict
    queue: list[int]


class WorkspaceSubjectRead(WorkspaceSubjectBase):
    id: int


class WorkspaceSubjectCreate(BaseModel):
    workspace_id: int | None
    ecourses_id: int | None = None
    name: str | None
    ecourses_link: str | None = None
    professor: str | None = None
    professor_contact: str | None = None
    requirements: str | None = None
