from src.core.database.models import User, Server as ServerModel
from src.core.exceptions import ServersFullError
from src.core.server import Server
from src.core.server.cookie.service import ServerCookieService
from src.core.server.dao import ServerDAO


class ServerService:
    def __init__(self, dao: ServerDAO, cookie_service: ServerCookieService):
        self._dao = dao
        self._cookie_service = cookie_service

    async def disable_user(self, user: User) -> None:
        server = await self._dao.get_server(server_id=user.server_id)
        await Server(server=server, cookie_service=self._cookie_service).delete_user(user=user)

    async def enable_user(self, user: User) -> None:
        if not user.server_id:
            server = await self._dao.get_available_server()

            if not server:
                raise ServersFullError(
                    "All server slots are occupied. " "Please add a server or increase the number of available seats."
                )

            await self._dao.set_user_server(server_id=server.id, user=user)

        server = await self._dao.get_server(server_id=user.server_id)
        await Server(server=server, cookie_service=self._cookie_service).add_user(user=user)

    async def get_sub_uri(self, server: ServerModel) -> str:
        default_settings = await Server(server=server, cookie_service=self._cookie_service).get_default_settings()
        return default_settings.sub_uri
