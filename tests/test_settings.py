from explore.env import AppEnv
from explore.settings import Settings


def test_db_echo_defaults_to_false() -> None:
    settings = Settings(app_env=AppEnv.TEST)

    assert settings.debug is True
    assert settings.db_echo is False


def test_db_echo_can_be_enabled() -> None:
    settings = Settings(app_env=AppEnv.TEST, db_echo="true")

    assert settings.db_echo is True
