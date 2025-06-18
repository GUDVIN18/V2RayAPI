from fastapi import APIRouter
from api.v2ray.routers import client_router

main_router = APIRouter()


main_router.include_router(client_router, tags=["Client requests"], prefix="/v2ray/client")