import json
import logging

import aiohttp

from src.core.database.models import Server as ServerModel, User
from src.core.server.cookie.service import ServerCookieService
from src.core.utils import generate_id_from_base

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, server: ServerModel, cookie_service: ServerCookieService):
        self.server = server
        self._cookie_service = cookie_service
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.server.cookie if self.server.cookie else "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }

    async def add_user(self, user: User):
        url = f"{self.server.domain}/panel/api/inbounds/addClient"
        user_data = {
            "id": self.server.connection_id,
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
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data=user_data, headers=self.headers)

            if response.status == 404:
                await self._cookie_service.handle_new_cookie(self_server=self)
                response = await session.post(url, data=user_data, headers=self.headers)

            text = await response.text()
            logger.info(text)
