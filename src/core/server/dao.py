from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import selectinload

from src.core import consts
from src.core.database.dao import BaseDAO
from src.core.database.models import Server as ServerModel
from src.core.database.models import Subscription, SubscriptionStatusType, User


class ServerDAO(BaseDAO):
    async def get_available_server(self):
        async for session in self._db.get_session():
            total_users_subq = select(func.count(User.id)).where(User.server_id == ServerModel.id).scalar_subquery()

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

            query = (
                select(ServerModel)
                .where(
                    total_users_subq < consts.LIMIT_TOTAL_USERS_ON_SERVER,
                    active_users_subq < consts.LIMIT_ACTIVE_USERS_ON_SERVER,
                )
                .order_by(active_users_subq.asc())
                .limit(1)
            )

            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_server(self, server_id) -> ServerModel:
        async for session in self._db.get_session():
            result = await session.execute(select(ServerModel).where(ServerModel.id == server_id))
        return result.scalar_one()

    async def set_user_server(self, user: User, server_id: int) -> User:
        async for session in self._db.get_session():
            user.server_id = server_id
            session.add(user)
            await session.commit()
