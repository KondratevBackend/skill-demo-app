import json
import logging

import aiohttp

from src.core.database.models import Server as ServerModel, User
from src.core.utils import generate_id_from_base

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, server: ServerModel):
        self._server = server
        self._headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': server.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def login(self):
        url = f"{self._server.domain}/login"
        data = {
            "username": "admin",
            "password": "admin",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=self._headers) as response:
                return response.cookies

    async def add_user(self, user: User):
        url = f"{self._server.domain}/panel/api/inbounds/addClient"
        user_data = {
            "id": self._server.connection_id,
            "settings": json.dumps({
                "clients": [
                    {
                        "id": str(user.telegram_id),
                        "flow": "xtls-rprx-vision",
                        "email": str(user.telegram_id),
                        "limitIp": 3,
                        "enable": True,
                        "subId": generate_id_from_base(user.id),
                    }
                ]
            })
        }
        xui_session = await self.login()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=user_data, cookies=xui_session) as response:
                text = await response.text()
                logger.info(text)
