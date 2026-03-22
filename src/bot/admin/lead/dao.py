from sqlalchemy import select, exists

from src.core.database.dao import BaseDAO
from src.core.database.models import Lead


class LeadAdminDAO(BaseDAO):
    async def exists_lead(self, url: str) -> bool:
        async for session in self._db.get_session():
            query = select(exists().where(Lead.url == url))
            result = await session.execute(query)
        return result.scalar_one()

    async def create_lead(self, title: str, url: str, description: str | None = None) -> None:
        async for session in self._db.get_session():
            instance = Lead(
                title=title,
                url=url,
                description=description,
            )
            session.add(instance)
            await session.commit()
