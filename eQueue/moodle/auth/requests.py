import requests

from core.schemas.moodle import MoodleLogin
from utils import build_auth_url, build_user_info_url
from .token_validator import validate


async def auth_by_moodle_credentials(credentials: MoodleLogin) -> str:
	auth_url = build_auth_url(
		login=credentials.login,
		password=credentials.password
	)
	response = requests.get(auth_url)

	response = response.json()
	await validate(
		response=response,
		error_key="error",
		message_key="error"
	)

	return response['token']


async def get_moodle_user_info(
		token: str,
		group_id: int
) -> dict:
	response = requests.get(build_user_info_url(token))

	response = response.json()
	await validate(response)

	return {
		"moodle_token": token,
		"ecourses_user_id": response["userid"],
		"assigned_group_id": group_id,
		"first_name": response["firstname"],
		"second_name": response["lastname"],
		# status will be added as defualt value
		"talon": response["username"],
		"user_picture_url": response["userpictureurl"]
	}
