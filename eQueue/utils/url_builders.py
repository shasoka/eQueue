#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from core.config import settings


def build_auth_url(login: str, password: str) -> str:
    return settings.moodle.auth_url % (login, password)


def build_user_info_url(token: str) -> str:
    return (
        f"{settings.moodle.ecourses_base_url}?"
        f"wstoken={token}&"
        f"wsfunction=core_webservice_get_site_info&"
        f"moodlewsrestformat=json"
    )
