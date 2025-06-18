from pydantic import BaseModel, Field
from typing import Optional, Any


class V2RayUserFromDB(BaseModel):
    uuid: str = Field(..., description="UUID пользователя")
    tg_id: int = Field(..., description="ID пользователя в Telegram")
    enable: bool = Field(..., description="Активировать пользователя")
    limit_ip: int = Field(..., description="Количество IP адресов, которые может использовать пользователь")
    expiry_time: int = Field(..., description="Время действия пользователя в мс (до какого числа будет активен)")

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None