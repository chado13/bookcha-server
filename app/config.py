from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    assistants_key: str
    db_pool_size: int = 5
    db_pool_max_overflow: int = 10
    auth_secret_key: str
    algorithm: str
    access_token_expired_minutes: int = 30

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(env_file="secrets/.env", extra="ignore")


CONFIG = Config()
