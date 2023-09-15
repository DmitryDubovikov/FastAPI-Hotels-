from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: str

    REDIS_HOST: str
    REDIS_PORT: str

    class Config:
        env_file: str = ".env"
        if __name__ == "__main__":
            env_file: str = "../.env"


settings = Settings()
print(settings.model_dump())

if __name__ == "__main__":
    print(settings.model_dump())
