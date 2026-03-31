from aiogram.types import User as TelegramUser
from sqlalchemy import desc, exists, select

from src.core.database.dao import BaseDAO
from src.core.database.models import Lead, LeadUser, Tariff, User


class StartDAO(BaseDAO):
    async def exists_user(self, telegram_id: int) -> bool:
        async for session in self._db.get_session():
            query = select(exists().where(User.telegram_id == telegram_id))
            result = await session.execute(query)
        return result.scalar_one()

    async def exists_lead_user(self, user_id: int, lead_id: int) -> bool:
        async for session in self._db.get_session():
            query = select(exists().where(LeadUser.user_id == user_id, LeadUser.lead_id == lead_id))
            result = await session.execute(query)
        return result.scalar_one()

    async def get_tariffs(self) -> list[Tariff]:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).order_by(Tariff.order_index))
        return result.scalars().all()

    async def get_lead_id_by_url_code(self, url_code: str) -> int | None:
        async for session in self._db.get_session():
            query = select(Lead.id).where(Lead.url.ilike(f"%{url_code}%"))
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, telegram_user: TelegramUser) -> User:
        async for session in self._db.get_session():
            instance = User(
                telegram_id=telegram_user.id,
                user_name=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )
            session.add(instance)
            await session.commit()
        return instance

    async def create_lead_user(self, lead_id: int, user_id: int) -> LeadUser:
        async for session in self._db.get_session():
            instance = LeadUser(
                user_id=user_id,
                lead_id=lead_id,
            )
            session.add(instance)
            await session.commit()
        return instance
