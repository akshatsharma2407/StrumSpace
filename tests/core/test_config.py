import pytest
from pydantic import SecretStr, ValidationError

from app.core.config import Settings
from app.core.config import TestDatabaseSettings as DatabaseTestSettings


def test_settings_use_ist_by_default() -> None:
    settings = Settings(_env_file=None)

    assert settings.timezone == "Asia/Kolkata"
    assert settings.api_v1_prefix == "/api/v1"


def test_settings_reject_invalid_timezone() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, timezone="Invalid/Timezone")


def test_settings_reject_empty_database_password() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, database_password=SecretStr(""))


def test_test_database_settings_require_explicit_database_configuration() -> None:
    settings = DatabaseTestSettings(
        database_host="localhost",
        database_name="strumspace_test",
        database_user="strumspace_test_user",
        database_password=SecretStr("test-password"),
    )

    assert settings.database_name == "strumspace_test"
