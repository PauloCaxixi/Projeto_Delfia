from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI

from app.api import documents_router
from app.core.logging_config import configure_logging
from app.database.init_db import init_database
from fastapi.middleware.cors import CORSMiddleware


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_database()
    yield


app = FastAPI(
    title="Encrypted Document Manager",
    description="API para gerenciamento seguro de documentos criptografados.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


app.include_router(documents_router)