from pydantic import BaseModel


class MoodleLogin(BaseModel):
	login: str
	password: str
