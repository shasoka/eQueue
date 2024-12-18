#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

import requests

from urllib.parse import quote_plus as url_encode

from moodle import proxies
from core.config import settings
from core.schemas.moodle import MoodleLogin
from utils import validate


async def auth_by_moodle_credentials(credentials: MoodleLogin) -> str:
    response = requests.get(
        settings.moodle.auth_url
        % (
            url_encode(credentials.login),
            url_encode(credentials.password),
        ),
        proxies=proxies,
    )

    response = response.json()
    await validate(response=response, error_key="error", message_key="error")

    return response["token"]


async def get_moodle_user_info(
    token: str,
) -> dict:
    """

    :param token:
    :type token:
    :return:
    :rtype:
    """

    response = requests.get(
        settings.moodle.get_user_info_url % url_encode(token),
        proxies=proxies,
    )

    response = response.json()
    await validate(response)

    return {
        "access_token": token,
        "ecourses_user_id": response["userid"],
        "first_name": response["firstname"],
        "second_name": response["lastname"],
        "talon": response["username"],
        "user_picture_url": response["userpictureurl"],
    }


async def token_persistence(token: str) -> None:
    response = requests.get(
        settings.moodle.get_user_info_url % url_encode(token),
        proxies=proxies,
    )
    response = response.json()
    await validate(response)
