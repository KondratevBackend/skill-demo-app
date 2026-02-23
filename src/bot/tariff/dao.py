from sqlalchemy import select, exists, and_
from sqlalchemy.orm import selectinload

from src.core.database.dao import BaseDAO
from src.core.database.models import Tariff, User, Subscription, SubscriptionStatusType


class BotTariffDAO(BaseDAO):
    async def exists_sub(self, user_id: int) -> bool:
        async for session in self._db.get_session():
            query = select(
                exists().where(
                    and_(
                        Subscription.user_id == user_id,
                        Subscription.status.in_(
                            (
                                SubscriptionStatusType.active,
                                SubscriptionStatusType.pending,
                            )
                        ),
                    )
                )
            )
            result = await session.execute(query)

        return result.scalar_one()

    async def get_user(self, telegram_id: int) -> User:
        async for session in self._db.get_session():
            query = (
                select(User)
                .options(selectinload(User.server))
                .where(User.telegram_id == telegram_id)
            )
            result = await session.execute(query)
        return result.scalar_one()

    async def get_tariff(self, tariff_id: int) -> Tariff:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        return result.scalar_one()
