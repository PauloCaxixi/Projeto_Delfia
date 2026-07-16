from cryptography.fernet import Fernet, InvalidToken


class EncryptionError(Exception):
    """Erro lançado quando uma operação de criptografia falha."""


class EncryptionService:
    """Responsável por criptografar e descriptografar documentos."""

    def __init__(self, encryption_key: str) -> None:
        if not encryption_key:
            raise ValueError("A chave de criptografia não pode estar vazia.")

        try:
            self._fernet = Fernet(encryption_key.encode("utf-8"))
        except (TypeError, ValueError) as error:
            raise ValueError("A chave de criptografia fornecida é inválida.") from error

    def encrypt(self, content: bytes) -> bytes:
        """Criptografa um conteúdo recebido em bytes."""

        if not content:
            raise ValueError("O conteúdo para criptografia não pode estar vazio.")

        try:
            return self._fernet.encrypt(content)
        except Exception as error:
            raise EncryptionError("Não foi possível criptografar o conteúdo.") from error

    def decrypt(self, encrypted_content: bytes) -> bytes:
        """Descriptografa um conteúdo e valida sua integridade."""

        if not encrypted_content:
            raise ValueError("O conteúdo criptografado não pode estar vazio.")

        try:
            return self._fernet.decrypt(encrypted_content)
        except InvalidToken as error:
            raise EncryptionError(
                "Não foi possível descriptografar o conteúdo."
            ) from error