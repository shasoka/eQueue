from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class APIv1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    moodle_auth: str = "/moodle_auth"
    token_persistence: str = "/token_persistence"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v1: APIv1Prefix = APIv1Prefix()
    token_url: str = "/api/v1/users/moodle_auth"


class MoodleAPI(BaseModel):
    auth_url: str = "https://e.sfu-kras.ru/login/token.php?service=moodle_mobile_app&username=%s&password=%s"
    timetable_url: str = "https://edu.sfu-kras.ru/api/timetable/get_insts"
    ecourses_base_url: str = "https://e.sfu-kras.ru/webservice/rest/server.php"
    upload_new_image_url: str = "https://e.sfu-kras.ru/webservice/upload.php?token=%s&filearea=draft"


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


settings = Settings()
