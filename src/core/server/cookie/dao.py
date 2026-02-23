from sqlalchemy import update

from src.core.database.dao import BaseDAO
from src.core.database.models import Server as ServerModel


class ServerCookieDAO(BaseDAO):
    async def update_cookie(self, server: ServerModel, cookie: str):
        async for session in self._db.get_session():
            server = await session.merge(server)
            server.cookie = cookie
            await session.commit()


        #     result = await session.execute(
        #         update(ServerModel)
        #         .where(ServerModel.id == server.id)
        #         .values(cookie=cookie)
        #         .returning(ServerModel)
        #     )
        #     instance = result.scalar_one()
        #     await session.commit()
        # return instance