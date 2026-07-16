from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def list_all(self) -> List[Document]:
        return (
            self.db.query(Document)
            .order_by(Document.created_at.desc())
            .all()
        )

    def get_by_id(self, document_id: str) -> Optional[Document]:
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def delete(self, document: Document) -> None:
        self.db.delete(document)
        self.db.commit()