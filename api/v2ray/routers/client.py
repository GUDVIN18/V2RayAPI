from typing import List
from fastapi import APIRouter, Depends, Path, status
from fastapi_restful.cbv import cbv
from loguru import logger as log
from api.v2ray.resources import service
from api.v2ray.resources.exceptions import *
from api.v2ray.resources.schemas import V2RayUserFromDB, SuccessResponse
from uuid import UUID

client_router = APIRouter()


@cbv(client_router)
class V2RayRouter:
    # prefix = "/v2ray/client"
    # conn: Connection = Depends(DBConnPool().get_connection)

    @client_router.post(
        "/create",
        response_model=V2RayUserFromDB,
        status_code=200,
        name="Создать пользователя VPN",
        description="Создает пользователя VPN",
    )
    async def create_v2ray_user(
        self,
        server_id: int = Path(..., description="ID сервера, на котором будет создан пользователь"),
        uuid: UUID = Path(..., description="UUID пользователя"),
        tg_id: int = Path(..., description="ID пользователя в Telegram"),
        enable: bool = Path(..., description="Активировать пользователя"),
        limit_ip: int = Path(..., description="Количество IP адресов, которые может использовать пользователь"),
        expiry_time: int = Path(..., description="Время действия пользователя в мс (до какого числа будет активен)"),
    ):
        status = await service.V2RayProccessor.create_v2ray_user(
            server_id=server_id,
            uuid=uuid, 
            tg_id=tg_id, 
            enable=enable,
            limit_ip=limit_ip,
            expiry_time=expiry_time
        )
        return status

    @client_router.post(
        "/update",
        response_model=V2RayUserFromDB,
        status_code=200,
        name="Обновить пользователя VPN",
        description="Обновляет пользователя VPN",
    )
    async def update_v2ray_user(
        self,
        server_id: int = Path(..., description="ID сервера, на котором будет создан пользователь"),
        tg_id: int = Path(..., description="ID пользователя в Telegram"),
        enable: bool = Path(..., description="Активировать пользователя"),
        limit_ip: int = Path(..., description="Количество IP адресов, которые может использовать пользователь"),
        expiry_time: int = Path(..., description="Время действия пользователя в мс (до какого числа будет активен)"),
    ):
        status = await service.V2RayProccessor.update_v2ray_user(
            server_id=server_id,
            tg_id=tg_id, 
            enable=enable,
            limit_ip=limit_ip,
            expiry_time=expiry_time
        )
        return status

    # @client_router.post(
    #     "/{device_id}/select",
    #     response_model=List[DeviceFromDB],
    #     name="Выбрать устройство",
    #     description="Позволяет пользователю выбрать новое устройство и деактивировать предыдущее "
    #     "выбранное устройство.",
    #     responses=get_exception_responses(*token_exceptions),
    # )
    # async def select_device(
    #     self,
    #     device_id: int = Path(..., description="ID девайса, который будет выбран"),
    #     user: TokenUser = Depends(token_access),
    # ) -> List[DeviceFromDB]:
    #     await service.select_device(conn=self.conn, device_id=device_id, user_id=user.id)
    #     return await DeviceCRUD.get_many(db=self.conn, user_id=user.id)

    # @client_router.delete(
    #     "/{device_id}",
    #     response_model=List[DeviceFromDB],
    #     name="Удалить устройство",
    #     description="Позволяет пользователю удалить устройство и его данные в Terra API",
    #     responses=get_exception_responses(DeviceNotFound, *token_exceptions),
    # )