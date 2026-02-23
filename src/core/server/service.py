from src.core import consts
from src.core.database.models import User
from src.core.exceptions import ServersFullError
from src.core.server import Server
from src.core.server.cookie.service import ServerCookieService
from src.core.server.dao import ServerDAO


class ServerService:
    def __init__(self, dao: ServerDAO, cookie_service: ServerCookieService):
        self._dao = dao
        self._cookie_service = cookie_service

    async def enable_user(self, user: User) -> bool:
        if not user.server_id:
            server = await self._dao.get_available_server()

            if not server:
                raise ServersFullError(
                    "All server slots are occupied. " "Please add a server or increase the number of available seats."
                )

            user = await self._dao.set_user_server(server_id=server.id, user_id=user.id)

        await Server(server=user.server, cookie_service=self._cookie_service).add_user(user=user)
