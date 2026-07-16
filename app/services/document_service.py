import hashlib
import uuid
from pathlib import Path
from typing import List, Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.encryption import EncryptionService
from app.models import Document
from app.repositories.document_repository import DocumentRepository


class DocumentNotFoundError(Exception):
    """Erro lançado quando um documento não é encontrado."""


class InvalidDocumentError(Exception):
    """Erro lançado quando o arquivo enviado é inválido."""


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)

        settings = get_settings()

        self.encryption_service = EncryptionService(
            settings.encryption_key
        )

        self.storage_directory = Path("storage")
        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload(self, uploaded_file: UploadFile) -> Document:
        original_name = uploaded_file.filename or "document.pdf"
        content_type = uploaded_file.content_type or ""

        self._validate_filename(original_name)
        self._validate_content_type(content_type)

        content = uploaded_file.file.read()

        self._validate_content(content)

        checksum = self._calculate_checksum(content)

        stored_name = f"{uuid.uuid4()}.enc"
        stored_path = self.storage_directory / stored_name

        encrypted_content = self.encryption_service.encrypt(content)

        stored_path.write_bytes(encrypted_content)

        document = Document(
            original_name=Path(original_name).name,
            stored_name=stored_name,
            content_type="application/pdf",
            size=len(content),
            checksum=checksum,
        )

        try:
            return self.repository.create(document)
        except Exception:
            if stored_path.exists():
                stored_path.unlink()

            raise

    def list_documents(self) -> List[Document]:
        return self.repository.list_all()

    def download(self, document_id: str) -> Tuple[Document, bytes]:
        document = self.repository.get_by_id(document_id)

        if document is None:
            raise DocumentNotFoundError(
                "Documento não encontrado."
            )

        stored_path = self.storage_directory / document.stored_name

        if not stored_path.exists():
            raise DocumentNotFoundError(
                "Arquivo criptografado não encontrado."
            )

        encrypted_content = stored_path.read_bytes()

        decrypted_content = self.encryption_service.decrypt(
            encrypted_content
        )

        return document, decrypted_content

    @staticmethod
    def _validate_filename(filename: str) -> None:
        if not filename.lower().endswith(".pdf"):
            raise InvalidDocumentError(
                "Somente arquivos PDF são permitidos."
            )

    @staticmethod
    def _validate_content_type(content_type: str) -> None:
        allowed_types = {
            "application/pdf",
            "application/octet-stream",
        }

        if content_type not in allowed_types:
            raise InvalidDocumentError(
                "O tipo do arquivo enviado não é permitido."
            )

    @staticmethod
    def _validate_content(content: bytes) -> None:
        if not content:
            raise InvalidDocumentError(
                "O arquivo enviado está vazio."
            )

        if not content.startswith(b"%PDF-"):
            raise InvalidDocumentError(
                "O arquivo enviado não possui conteúdo PDF válido."
            )

        maximum_size = 10 * 1024 * 1024

        if len(content) > maximum_size:
            raise InvalidDocumentError(
                "O arquivo excede o limite de 10 MB."
            )

    @staticmethod
    def _calculate_checksum(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()