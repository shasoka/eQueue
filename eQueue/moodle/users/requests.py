#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

import requests

from moodle.proxies import proxies
from core.config import settings
from utils import validate


async def patch_profile_picture(
    token: str,
    files: dict,
) -> str:
    response = requests.post(
        settings.moodle.upload_new_image_url % token,
        files=files,
        proxies=proxies,
    )
    response = response.json()
    if not isinstance(response, list):
        await validate(response)

    response_data = response[0]
    draftitemid = response_data.get("itemid")

    upd_data = {
        "draftitemid": draftitemid,
        "wsfunction": "core_user_update_picture",
        "wstoken": token,
        "moodlewsrestformat": "json",
    }

    response = requests.post(
        settings.moodle.ecourses_base_url,
        data=upd_data,
        proxies=proxies,
    )
    response = response.json()
    await validate(response, error_key="error", message_key="error")

    return response.get("profileimageurl")
