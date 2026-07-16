from typing import Dict

from fastapi import FastAPI


app = FastAPI(
    title="Encrypted Document Manager",
    description="API para gerenciamento seguro de documentos criptografados.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Verifica se a aplicação está funcionando."""

    return {"status": "healthy"}