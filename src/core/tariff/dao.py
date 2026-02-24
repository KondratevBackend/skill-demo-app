import datetime

from sqlalchemy import and_, exists, or_, select

from src.core.database.dao import BaseDAO
from src.core.database.models import Subscription, SubscriptionStatusType, Tariff, User


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

    async def add_sub(
        self,
        user_id: int,
        tariff: Tariff,
        status: SubscriptionStatusType,
        starts_at: datetime.datetime = None,
        expires_at: datetime.datetime = None,
    ) -> Subscription:
        async for session in self._db.get_session():
            instance = Subscription(
                user_id=user_id,
                tariff_id=tariff.id,
                status=status,
                starts_at=starts_at,
                expires_at=expires_at,
            )
            session.add(instance)
            await session.commit()
        return instance
