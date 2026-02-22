import logging

import aiohttp

from src.core.database.models import Server as ServerModel, User

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, server: ServerModel):
        self._server = server
        self._headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': server.cookie,
        }

    async def add_user(self, user: User):
        url = f"{self._server.domain}/panel/inbound/addClient"
        user_data = {
            "id": [self._server.connection_id],
            "settings": [
                {
                    "clients": [
                        {
                            "id": user.telegram_id,
                            "flow": "xtls-rprx-vision",
                            "email": user.telegram_id,
                            "limitIp": 3,
                            "enable": "true",
                            "subId": user.id,
                        }
                    ]
                }
            ]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=user_data, headers=self._headers) as response:
                if response.status == 404:
                    raise ConnectionError
                text = await response.text()
                logger.info(text)

