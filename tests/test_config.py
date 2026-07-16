from cryptography.fernet import Fernet

from app.core.config import Settings


def test_settings_should_accept_valid_configuration() -> None:
    encryption_key = Fernet.generate_key().decode("utf-8")

    settings = Settings(
        encryption_key=encryption_key,
        api_username="test-user",
        api_password="test-password",
        _env_file=None,
    )

    assert settings.encryption_key == encryption_key
    assert settings.api_username == "test-user"
    assert settings.api_password == "test-password"