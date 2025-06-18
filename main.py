import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from loguru import logger as log

from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from api.router import main_router


app = FastAPI(
    title="Microservice W_VPN data API methods",
    version="0.1.0",
    openapi_tags=[{"name": "W_VPN", "description": "W_VPN connection Management"}],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CorrelationIdMiddleware,
    # The HTTP header key to read IDs from.
    header_name="X-Request-ID",
)

app.include_router(main_router)


if __name__ == "__main__":
    log.info("Starting debug uvicorn")
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8080,
        reload=True,
        workers=1,
        log_level='debug',
    )
    log.info("Uvicorn stopped")
