import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    original_name = Column(
        String,
        nullable=False,
    )

    stored_name = Column(
        String,
        nullable=False,
        unique=True,
    )

    content_type = Column(
        String,
        nullable=False,
    )

    size = Column(
        Integer,
        nullable=False,
    )

    checksum = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )