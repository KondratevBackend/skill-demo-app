from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from src.core.database.dao import BaseDAO
from src.core.database.models import Subscription, SubscriptionStatusType, User


class LKDAO(BaseDAO):
    async def get_user(self, telegram_id: int) -> User:
        async for session in self._db.get_session():
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
        return result.scalar_one()

    async def get_pending_subscription(self, user_id: int) -> list[Subscription]:
        async for session in self._db.get_session():
            query = (
                select(Subscription)
                .options(joinedload(Subscription.tariff))
                .where(
                    Subscription.user_id == user_id,
                    Subscription.status == SubscriptionStatusType.pending,
                )
            )
            result = await session.execute(query)
        return result.scalars().all()

    async def get_active_subscription(self, user_id: int) -> Subscription:
        async for session in self._db.get_session():
            query = (
                select(Subscription)
                .options(joinedload(Subscription.tariff))
                .where(
                    Subscription.user_id == user_id,
                    Subscription.status == SubscriptionStatusType.active,
                )
            )
            result = await session.execute(query)
        return result.scalar_one_or_none()
