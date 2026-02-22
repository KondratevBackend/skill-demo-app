import datetime

from sqlalchemy import select, exists, or_, and_

from src.core.database.dao import BaseDAO
from src.core.database.models import User, Subscription, SubscriptionStatusType, Tariff


class TariffDAO(BaseDAO):
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

    async def add_sub(self, user_id: int, tariff: Tariff, status: SubscriptionStatusType) -> Subscription:
        async for session in self._db.get_session():
            instance = Subscription(
                user_id=user_id,
                tariff_id=tariff.id,
                status=status,
                starts_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now() + datetime.timedelta(days=tariff.days),
            )
            session.add(instance)
            await session.commit()
        return instance
