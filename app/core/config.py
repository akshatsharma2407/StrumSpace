from functools import lru_cache
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "StrumSpace API"
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "staging", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    api_v1_prefix: str = "/api/v1"
    timezone: str = "Asia/Kolkata"
    database_host: str = "localhost"
    database_port: int = Field(default=3307, ge=1, le=65535)
    database_name: str = "strumspace"
    database_user: str = "strumspace_user"
    database_password: SecretStr = SecretStr("YOUR_STRONG_PASSWORD")
    database_pool_size: int = Field(default=5, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)
    database_pool_timeout: float = Field(default=30.0, gt=0)
    database_pool_recycle: int = Field(default=1800, ge=0)
    database_echo: bool = False

    @field_validator("database_name", "database_user")
    @classmethod
    def validate_database_identifier(cls, value: str) -> str:
        if not value or not value.replace("_", "").isalnum():
            raise ValueError("Database names and users may contain only letters, numbers, and underscores")
        return value

    @field_validator("database_host")
    @classmethod
    def validate_database_host(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Database host must not be empty")
        return value

    @field_validator("database_password")
    @classmethod
    def validate_database_password(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value():
            raise ValueError("Database password must not be empty")
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="STRUMSPACE_",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Invalid IANA timezone: {value}") from exc
        return value


class TestDatabaseSettings(BaseSettings):
    """Explicit configuration for the isolated MySQL test database."""

    database_host: str = 'localhost'
    database_port: int = Field(default=3307, ge=1, le=65535)
    database_name: str = 'strumspace_test'
    database_user: str = 'strumspace_test_user'
    database_password: SecretStr = 'test_password'
    database_pool_size: int = Field(default=5, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)
    database_pool_timeout: float = Field(default=30.0, gt=0)
    database_pool_recycle: int = Field(default=1800, ge=0)
    database_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="STRUMSPACE_TEST_",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("database_name", "database_user")
    @classmethod
    def validate_database_identifier(cls, value: str) -> str:
        if not value or not value.replace("_", "").isalnum():
            raise ValueError("Database names and users may contain only letters, numbers, and underscores")
        return value

    @field_validator("database_host")
    @classmethod
    def validate_database_host(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Database host must not be empty")
        return value

    @field_validator("database_password")
    @classmethod
    def validate_database_password(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value():
            raise ValueError("Database password must not be empty")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
