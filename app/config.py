from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str | None = None
    database_username: str | None = None
    secret_key: str | None = None
    algorithm: str | None = None
    access_token_expire_minutes: int | None = None

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
