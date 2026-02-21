from aiogram.types import User as TelegramUser
from sqlalchemy import exists, select, desc

from src.core.database.dao import BaseDAO
from src.core.database.models import Tariff, User


class StartDAO(BaseDAO):
    async def exists_user(self, telegram_id: int) -> bool:
        async for session in self._db.get_session():
            query = select(exists().where(User.telegram_id == telegram_id))
            result = await session.execute(query)
        return result.scalar_one()

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

    async def get_tariffs(self) -> list[Tariff]:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).order_by(Tariff.order_index))
        return result.scalars().all()
