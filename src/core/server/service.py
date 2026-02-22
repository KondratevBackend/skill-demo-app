from src.core import consts
from src.core.database.models import User
from src.core.exceptions import ServersFullError
from src.core.server import Server
from src.core.server.dao import ServerDAO


class ServerService:
    def __init__(self, dao: ServerDAO):
        self._dao = dao

    async def enable_user(self, user: User) -> bool:
        if not user.server_id:
            server = await self._dao.get_available_server()

            if not server:
                raise ServersFullError(
                    "All server slots are occupied. "
                    "Please add a server or increase the number of available seats."
                )

            user = await self._dao.set_user_server(server_id=server.id, user_id=user.id)

        server = await self._dao.get_server(server_id=user.server_id)
        await Server(server=server).add_user(user=user)
