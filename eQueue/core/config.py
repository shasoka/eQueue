from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
	host: str = "0.0.0.0"
	port: int = 8000


class APIPrefix(BaseModel):
	prefix: str = "/api"


class DatabaseConfig(BaseModel):
	url: PostgresDsn
	echo: bool = False
	echo_pool: bool = False
	max_overflow: int = 10
	pool_size: int = 50


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=(".env-template", ".env"),
		case_sensitive=False,  # In .env uppercase preferred, in code lowercase
		env_nested_delimiter="__",  # Nested vars
		env_prefix="APP_CONFIG__"  # Prefix for env vars
	)

	run: RunConfig = RunConfig()
	api: APIPrefix = APIPrefix()
	db: DatabaseConfig


settings = Settings()
