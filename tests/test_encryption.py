import pytest
from cryptography.fernet import Fernet

from app.core.encryption import EncryptionError, EncryptionService


@pytest.fixture
def encryption_key() -> str:
    """Fornece uma chave segura para os testes."""

    return Fernet.generate_key().decode("utf-8")


@pytest.fixture
def encryption_service(
    encryption_key: str,
) -> EncryptionService:
    """Cria o serviço usado pelos testes."""

    return EncryptionService(encryption_key)


def test_encrypt_returns_content_different_from_original(
    encryption_service: EncryptionService,
) -> None:
    original_content = b"Documento confidencial"

    encrypted_content = encryption_service.encrypt(original_content)

    assert encrypted_content != original_content


def test_decrypt_restores_original_content(
    encryption_service: EncryptionService,
) -> None:
    original_content = b"Documento confidencial"

    encrypted_content = encryption_service.encrypt(original_content)
    decrypted_content = encryption_service.decrypt(encrypted_content)

    assert decrypted_content == original_content


def test_decrypt_fails_with_different_key(
    encryption_service: EncryptionService,
) -> None:
    encrypted_content = encryption_service.encrypt(
        b"Documento confidencial"
    )

    different_key = Fernet.generate_key().decode("utf-8")
    different_service = EncryptionService(different_key)

    with pytest.raises(EncryptionError):
        different_service.decrypt(encrypted_content)


def test_decrypt_fails_when_content_is_modified(
    encryption_service: EncryptionService,
) -> None:
    encrypted_content = encryption_service.encrypt(
        b"Documento confidencial"
    )

    modified_content = encrypted_content[:-1] + b"x"

    with pytest.raises(EncryptionError):
        encryption_service.decrypt(modified_content)


def test_encrypt_rejects_empty_content(
    encryption_service: EncryptionService,
) -> None:
    with pytest.raises(
        ValueError,
        match="O conteúdo para criptografia não pode estar vazio",
    ):
        encryption_service.encrypt(b"")


def test_decrypt_rejects_empty_content(
    encryption_service: EncryptionService,
) -> None:
    with pytest.raises(
        ValueError,
        match="O conteúdo criptografado não pode estar vazio",
    ):
        encryption_service.decrypt(b"")


def test_service_rejects_empty_key() -> None:
    with pytest.raises(
        ValueError,
        match="A chave de criptografia não pode estar vazia",
    ):
        EncryptionService("")


def test_service_rejects_invalid_key() -> None:
    with pytest.raises(
        ValueError,
        match="A chave de criptografia fornecida é inválida",
    ):
        EncryptionService("chave-invalida")