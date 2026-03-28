from sqlalchemy import select

from src.core.database import Database


class BaseDAO:
    model = None

    def __init__(self, db: Database):
        self._db = db

    async def get_all(self, **where):
        async for session in self._db.get_session():
            query = select(self.model).where(**where)
            result = await session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, model_id: int):
        async for session in self._db.get_session():
            query = select(self.model).where(self.model.id == model_id)
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, **data) -> None:
        async for session in self._db.get_session():
            new_record = self.model(**data)
            session.add(new_record)
            await session.commit()
