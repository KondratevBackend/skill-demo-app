import asyncio
import logging

import aiohttp

from src.core.config import ServerSettings
from src.core.database.models import Server as ServerModel
from src.core.exceptions import ServerReloginFailedError
from src.core.server.cookie.dao import ServerCookieDAO


logger = logging.getLogger(__name__)


class ServerCookieService:
    _relogin_lock = asyncio.Lock()

    def __init__(self, dao: ServerCookieDAO, config: ServerSettings):
        self._dao = dao
        self._config = config

    async def __relogin(self, server: ServerModel):
        url = f"{server.domain}/login"
        data = {
            "username": self._config.username,
            "password": self._config.password,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                return response.headers

    @staticmethod
    async def __test_cookie(server: ServerModel, cookie: str):
        url = f"{server.domain}/panel/api/inbounds/list"
        test_headers = {
            "Content-Type": "application/json",
            "Cookie": cookie,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=test_headers) as response:
                return response.status

    async def handle_new_cookie(self, self_server):
        async with self._relogin_lock:
            logger.info(f"Updating cookie on the server {self_server.server.id=}")
            headers = await self.__relogin(server=self_server.server)
            new_cookie = headers["Set-Cookie"]
            cookie_test_status_code = await self.__test_cookie(server=self_server.server, cookie=new_cookie)
            if cookie_test_status_code == 200:
                await self._dao.update_cookie(cookie=new_cookie, server=self_server.server)
                self_server.headers["Cookie"] = new_cookie
            else:
                logger.warning(
                    f"Failed to refresh cookie for server {self_server.server.id=}. "
                    f"Test status code: {cookie_test_status_code}. "
                    f"Relogin was unsuccessful."
                )
                raise ServerReloginFailedError(f"Failed to refresh cookie for server {self_server.server.id=}")
