import os
from py3xui import Api, Client
from api.v2ray.resources.schemas import SuccessResponse
from asgiref.sync import sync_to_async
import qrcode
from py3xui import Inbound

#Временно сделаем через django ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_builder.settings')
import django
django.setup()
from .....bot_builder.apps.xrey_app import VPNServer
# 


class V2RayProccessor:

    async def create_v2ray_user(
        self,
        server_id: int,
        uuid: str,
        tg_id: int,
        enable: bool,
        limit_ip: int,
        expiry_time: int
        ):
        server: VPNServer = await sync_to_async(VPNServer.objects.get)(id=server_id)

        # Login to XUI
        os.environ["XUI_HOST"] = server.xui_host
        os.environ["XUI_USERNAME"] = server.xui_username
        os.environ["XUI_PASSWORD"] = server.xui_password
        XUI_EXTERNAL_IP = server.xui_external_ip
        MAIN_REMARK = server.main_remark
        SERVER_PORT = str(server.port_client)
        inbound_id = server.inbound_id
        api = Api.from_env()
        api.login()
        inbound = api.inbound.get_by_id(inbound_id)

        new_client = Client(
            id=uuid,
            email=str(tg_id),
            enable=enable,
            flow="xtls-rprx-vision",
            tg_id=tg_id,
            limit_ip=limit_ip,
            level=0,
            expiry_time=expiry_time
        )
        key = await get_connection_string(
            inbound, uuid, str(tg_id),
            XUI_EXTERNAL_IP, SERVER_PORT, MAIN_REMARK
        )
        qrcode_path = await generate_qr_code_async(key, str(tg_id), output_dir="./vpn/qrcodes")
        try:
            api.client.add(inbound_id, [new_client])

        except Exception as e:
            raise e
        return SuccessResponse(
            message="Success Create",
            data={"key": key, "qrcode_path": qrcode_path}
        )

    async def update_v2ray_user(
        self,
        server_id: int,
        tg_id: int,
        enable: bool,
        limit_ip: int,
        expiry_time: int
    ):
        server: VPNServer = await sync_to_async(VPNServer.objects.get)(id=server_id)

        # Login to XUI
        os.environ["XUI_HOST"] = server.xui_host
        os.environ["XUI_USERNAME"] = server.xui_username
        os.environ["XUI_PASSWORD"] = server.xui_password
        XUI_EXTERNAL_IP = server.xui_external_ip
        MAIN_REMARK = server.main_remark
        SERVER_PORT = str(server.port_client)
        inbound_id = server.inbound_id
        api = Api.from_env()
        api.login()
        inbound = api.inbound.get_by_id(inbound_id)

        clients = inbound.settings.clients
        for client in clients:
            if client.email == str(tg_id):
                # if await user_condition(str(tg_id)) == "Платно":
                client.inbound_id = inbound_id
                user_uuid = client.id
                client.enable = enable
                client.limit_ip = limit_ip
                client.expiry_time = expiry_time
                api.client.update(str(client.id), client)

                return SuccessResponse(
                    message="Success Update",
                    data={**client.dict()}
                )
        if not clients:
            raise ValueError("clients not found")





async def generate_qr_code_async(data: str, tg_id: str, output_dir: str = "qrcodes") -> str:
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    img = qrcode.make(data)
    file_path = os.path.join(output_dir, f"{tg_id}.png")
    img.save(file_path)
    return file_path
    
async def get_connection_string(inbound: Inbound, user_uuid: str, user_email: str,
                          XUI_EXTERNAL_IP: str, SERVER_PORT: str,
                          MAIN_REMARK: str) -> str:
    public_key = inbound.stream_settings.reality_settings.get("settings").get("publicKey")
    website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
    short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]

    connection_string = (
        f"vless://{user_uuid}@{XUI_EXTERNAL_IP}:{SERVER_PORT}"
        f"?type=tcp&security=reality&pbk={public_key}&fp=chrome&sni={website_name}"
        f"&sid={short_id}&spx=%2F&flow=xtls-rprx-vision#{MAIN_REMARK}-{user_email}"
    )
    return connection_string