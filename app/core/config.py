from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_ASYNC_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_URL: str

    RABBITMQ_URL: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    EMAIL_FROM: str
    EMAIL_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
