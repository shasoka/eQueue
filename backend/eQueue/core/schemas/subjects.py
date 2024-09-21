#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel

from core.schemas.subject_assignments import SubjectAssignmentRead


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


class WorkspaceSubjectWithAssignmentsRead(WorkspaceSubjectRead):
    assignments: list[SubjectAssignmentRead]


class WorkspaceSubjectCreate(BaseModel):
    workspace_id: int | None
    ecourses_id: int | None = None
    name: str | None
    ecourses_link: str | None = None
    professor: str | None = None
    professor_contact: str | None = None
    requirements: str | None = None


class WorkspaceSubjectUpdate(BaseModel):
    id: int
    workspace_id: int
    professor: str | None = None
    professor_contact: str | None = None
    requirements: str | None = None
    ecourses_link: str | None = None
    name: str | None = None
