from sqlalchemy import update

from src.core.database.dao import BaseDAO
from src.core.database.models import Server as ServerModel


class ServerCookieDAO(BaseDAO):
    async def update_cookie(self, server: ServerModel, cookie: str):
        async for session in self._db.get_session():
            server = await session.merge(server)
            server.cookie = cookie
            await session.commit()
