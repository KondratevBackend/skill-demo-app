from sqlalchemy import select, exists, and_, func, or_
from sqlalchemy.orm import selectinload

from src.core import consts
from src.core.database.dao import BaseDAO
from src.core.database.models import Tariff, User, Subscription, SubscriptionStatusType, Server as ServerModel


class BotTariffDAO(BaseDAO):
    async def exists_available_server(self) -> bool:
        async for session in self._db.get_session():
            total_users_subq = (
                select(func.count(User.id))
                .where(User.server_id == ServerModel.id)
                .scalar_subquery()
            )

            active_users_subq = (
                select(func.count(func.distinct(User.id)))
                .join(Subscription, Subscription.user_id == User.id)
                .where(
                    User.server_id == ServerModel.id,
                    or_(
                        Subscription.status == SubscriptionStatusType.active,
                        Subscription.status == SubscriptionStatusType.pending,
                    ),
                )
                .scalar_subquery()
            )

            exists_query = select(
                exists(
                    select(ServerModel.id).where(
                        total_users_subq < consts.LIMIT_TOTAL_USERS_ON_SERVER,
                        active_users_subq < consts.LIMIT_ACTIVE_USERS_ON_SERVER,
                    )
                )
            )

            result = await session.execute(exists_query)
        return result.scalar()

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
                .where(User.telegram_id == telegram_id)
            )
            result = await session.execute(query)
        return result.scalar_one()

    async def get_tariff(self, tariff_id: int) -> Tariff:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        return result.scalar_one()
