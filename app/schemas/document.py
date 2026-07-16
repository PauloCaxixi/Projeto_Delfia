from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: str
    original_name: str
    content_type: str
    size: int
    checksum: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)