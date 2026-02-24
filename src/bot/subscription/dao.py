from sqlalchemy import select

from src.core.database.dao import BaseDAO
from src.core.database.models import Server


class SubscriptionDAO(BaseDAO):
    async def get_server(self, server_id) -> Server:
        async for session in self._db.get_session():
            result = await session.execute(select(Server).where(Server.id == server_id))
        return result.scalar_one()
