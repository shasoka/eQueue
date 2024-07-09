from pydantic import BaseModel


class MoodleLogin(BaseModel):
    login: str
    password: str


class MoodleTokenMixin(BaseModel):
    access_token: str
