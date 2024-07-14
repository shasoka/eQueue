#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    # For development
    host: str = "127.0.0.1"
    port: int = 8000


class APIv1Prefix(BaseModel):
    prefix: str = "/v1"
    users_prefix: str = "/users"
    groups_prefix: str = "/groups"
    workspaces_prefix: str = "/workspaces"
    subjects_prefix: str = "/subjects"
    websocket_prefix: str = "/queue_ws"

    moodle_auth: str = "/moodle_auth"
    token_persistence_head: str = "/token_persistence"
    join_workspace: str = "/join"
    accept_pending: str = "/accept/{user_id}"
    leave_workspace: str = "/leave/{user_id}"
    raise_up_user: str = "/raise/{user_id}"
    ecourses_enrolled: str = "/enrolled"
    get_user_submissions: str = "/submissions"
    gen_subject_assignments: str = "/assignments/generate"
    add_subject_assignments: str = "/assignments"
    update_subject_assignments: str = "/assignments"
    mark_assignment: str = "/assignments/mark"
    delete_subject_assignment: str = "/assignments/{assignment_id}"
    get_current_queue_state: str = "/{subject_id}"
    patch_queue_enter: str = "/enter/{subject_id}"
    patch_queue_leave: str = "/leave/{subject_id}"
    patch_queue_leave_and_mark: str = "/leave/mark/{subject_id}"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v1: APIv1Prefix = APIv1Prefix()
    token_url: str = "/api/v1/users/moodle_auth"


class MoodleAPI(BaseModel):
    auth_url: str = (
        "https://e.sfu-kras.ru/login/token.php"
        "?service=moodle_mobile_app"
        "&username=%s"
        "&password=%s"
    )
    timetable_url: str = "https://edu.sfu-kras.ru/api/timetable/get_insts"
    ecourses_base_url: str = "https://e.sfu-kras.ru/webservice/rest/server.php"
    get_user_info_url: str = (
        f"{ecourses_base_url}?wstoken=%s&wsfunction=core_webservice_get_site_info&moodlewsrestformat=json"
    )
    upload_new_image_url: str = (
        "https://e.sfu-kras.ru/webservice/upload.php" "?token=%s" "&filearea=draft"
    )
    enrolled_courses_url: str = (
        "https://e.sfu-kras.ru/webservice/rest/server.php"
        "?wstoken=%s"
        "&wsfunction=core_enrol_get_users_courses"
        "&moodlewsrestformat=json"
        "&userid=%d"
    )
    course_structure: str = (
        "https://e.sfu-kras.ru/webservice/rest/server.php"
        "?wstoken=%s"
        "&wsfunction=core_course_get_contents"
        "&moodlewsrestformat=json"
        "&courseid=%d"
    )
    course_url: str = "https://e.sfu-kras.ru/course/view.php?id=%s"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Proxy(BaseModel):
    http: str
    https: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env-template", ".env"),
        case_sensitive=False,  # In .env uppercase preferred, in code lowercase
        env_nested_delimiter="__",  # Nested vars
        env_prefix="APP_CONFIG__",  # Prefix for env vars
    )

    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    moodle: MoodleAPI = MoodleAPI()
    db: DatabaseConfig
    proxy: Proxy


settings = Settings()
