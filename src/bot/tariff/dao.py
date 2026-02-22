from sqlalchemy import select

from src.core.database.dao import BaseDAO
from src.core.database.models import User, Tariff


class BotTariffDAO(BaseDAO):
    async def get_user(self, telegram_id: int) -> User:
        async for session in self._db.get_session():
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one()

    async def get_tariff(self, tariff_id: int) -> Tariff:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        return result.scalar_one()

