from app.database import Base, engine
from app.models import Document


def init_database() -> None:
    Base.metadata.create_all(bind=engine)