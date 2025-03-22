from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="./secretes/.env", extra="ignore")

    assistants_key: str = ""

CONFIG = Config()