#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel


class UserSubmissionBase(BaseModel):
    user_id: int
    workspace_id: int
    subject_id: int
    total_required_works: int
    submitted_works: list[int]


class UserSubmissionRead(UserSubmissionBase):
    id: int


class UserSubmissionUpdate(BaseModel):
    user_id: int
    workspace_id: int
    subject_id: int
    assignment_id: int
