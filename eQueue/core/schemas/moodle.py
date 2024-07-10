#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>
#
from pydantic import BaseModel


class MoodleLogin(BaseModel):
    login: str
    password: str


class MoodleTokenMixin(BaseModel):
    access_token: str


class EcoursesSubjectDescription(BaseModel):
    id: int | None
    shortname: str | None
    fullname: str | None
    displayname: str | None
    lastaccess: int | None
    isfavourite: bool | None
    hidden: bool | None


class EcourseSubjectModule(BaseModel):
    url: str
    name: str


class EcoursesSubjectStructure(BaseModel):
    assign_modules: list[EcourseSubjectModule]


class SelectedCourses(BaseModel):
    courses: list[int]
