from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_url: str
    assistants_key: str
    db_pool_size: int = 5
    db_pool_max_overflow: int = 10

    model_config = SettingsConfigDict(env_file="secrets/.env", extra="ignore")


CONFIG = Config()
