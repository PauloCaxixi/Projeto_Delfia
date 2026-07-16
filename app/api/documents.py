import logging
from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.authentication import authenticate_user
from app.database.session import get_db
from app.schemas import DocumentResponse
from app.services.document_service import (
    DocumentNotFoundError,
    DocumentService,
    InvalidDocumentError,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    username: str = Depends(authenticate_user),
) -> DocumentResponse:
    service = DocumentService(db)

    try:
        document = service.upload(file)

        logger.info(
            "Document uploaded",
            extra={
                "document_id": document.id,
                "username": username,
            },
        )

        return document

    except InvalidDocumentError as error:
        logger.warning(
            "Document upload rejected",
            extra={"username": username},
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=List[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    username: str = Depends(authenticate_user),
) -> List[DocumentResponse]:
    service = DocumentService(db)
    documents = service.list_documents()

    logger.info(
        "Documents listed",
        extra={"username": username},
    )

    return documents


@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    db: Session = Depends(get_db),
    username: str = Depends(authenticate_user),
) -> StreamingResponse:
    service = DocumentService(db)

    try:
        document, content = service.download(document_id)

        logger.info(
            "Document downloaded",
            extra={
                "document_id": document.id,
                "username": username,
            },
        )

        return StreamingResponse(
            BytesIO(content),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{document.original_name}"'
                )
            },
        )

    except DocumentNotFoundError as error:
        logger.warning(
            "Document download failed",
            extra={
                "document_id": document_id,
                "username": username,
            },
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error