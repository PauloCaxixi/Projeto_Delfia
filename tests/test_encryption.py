import pytest
from cryptography.fernet import Fernet

from app.core.encryption import EncryptionError, EncryptionService


@pytest.fixture
def encryption_key() -> str:
    """Fornece uma chave segura para cada teste."""

    return Fernet.generate_key().decode("utf-8")


@pytest.fixture
def encryption_service(encryption_key: str) -> EncryptionService:
    """Cria o serviço de criptografia utilizado nos testes."""

    return EncryptionService(encryption_key)


def test_encrypt_should_return_content_different_from_original(
    encryption_service: EncryptionService,
) -> None:
    original_content = b"Documento confidencial"

    encrypted_content = encryption_service.encrypt(original_content)

    assert encrypted_content != original_content


def test_decrypt_should_restore_original_content(
    encryption_service: EncryptionService,
) -> None:
    original_content = b"Documento confidencial"

    encrypted_content = encryption_service.encrypt(original_content)
    decrypted_content = encryption_service.decrypt(encrypted_content)

    assert decrypted_content == original_content


def test_decrypt_should_fail_with_different_key(
    encryption_service: EncryptionService,
) -> None:
    encrypted_content = encryption_service.encrypt(b"Documento confidencial")

    different_key = Fernet.generate_key().decode("utf-8")
    different_service = EncryptionService(different_key)

    with pytest.raises(EncryptionError):
        different_service.decrypt(encrypted_content)


def test_decrypt_should_fail_when_content_is_modified(
    encryption_service: EncryptionService,
) -> None:
    encrypted_content = encryption_service.encrypt(b"Documento confidencial")
    modified_content = encrypted_content[:-1] + b"x"

    with pytest.raises(EncryptionError):
        encryption_service.decrypt(modified_content)


def test_encrypt_should_reject_empty_content(
    encryption_service: EncryptionService,
) -> None:
    with pytest.raises(
        ValueError,
        match="O conteúdo para criptografia não pode estar vazio",
    ):
        encryption_service.encrypt(b"")


def test_service_should_reject_empty_key() -> None:
    with pytest.raises(
        ValueError,
        match="A chave de criptografia não pode estar vazia",
    ):
        EncryptionService("")