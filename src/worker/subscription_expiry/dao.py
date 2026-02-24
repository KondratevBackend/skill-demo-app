import datetime

from sqlalchemy import select, update, and_
from sqlalchemy.orm import joinedload

from src.core.database.dao import BaseDAO
from src.core.database.models import Subscription, SubscriptionStatusType, User


class SubscriptionExpiryWorkerDAO(BaseDAO):
    async def get_user(self, user_id: int):
        async for session in self._db.get_session():
            query = (
                select(User)
                .where(User.id == user_id)
            )
            result = await session.execute(query)
        return result.scalar_one()

    async def get_subscriptions_with_expire_data_and_active(self) -> list[Subscription]:
        async for session in self._db.get_session():
            query = (
                select(Subscription)
                .where(
                    and_(
                        Subscription.status == SubscriptionStatusType.active,
                        Subscription.expires_at <= datetime.datetime.now(),
                    )
                )
            )
            result = await session.execute(query)
        return result.scalars().all()

    async def get_earliest_pending_subscription(self, user_id: int) -> Subscription:
        async for session in self._db.get_session():
            query = (
                select(Subscription)
                .options(joinedload(Subscription.tariff))
                .where(
                    and_(
                        Subscription.user_id == user_id,
                        Subscription.status == SubscriptionStatusType.pending,
                    )
                )
                .order_by(Subscription.created_at)
            )
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def deactivate_subscription(self, subscription_id: int) -> None:
        async for session in self._db.get_session():
            query = (
                update(Subscription)
                .where(Subscription.id == subscription_id)
                .values(status=SubscriptionStatusType.expired)
            )
            await session.execute(query)
            await session.commit()

    async def activate_subscription(self, subscription: Subscription) -> None:
        async for session in self._db.get_session():
            query = (
                update(Subscription)
                .where(Subscription.id == subscription.id)
                .values(
                    status=SubscriptionStatusType.active,
                    starts_at=datetime.datetime.now(),
                    expires_at=datetime.datetime.now() + datetime.timedelta(days=subscription.tariff.days),
                )
            )
            await session.execute(query)
            await session.commit()
