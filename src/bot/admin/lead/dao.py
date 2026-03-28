from sqlalchemy import select, exists, func
from sqlalchemy.orm import joinedload

from src.core.database.dao import BaseDAO
from src.core.database.models import Lead, LeadUser, User, Subscription, Tariff


class LeadAdminDAO(BaseDAO):
    async def exists_lead(self, url: str) -> bool:
        async for session in self._db.get_session():
            query = select(exists().where(Lead.url == url))
            result = await session.execute(query)
        return result.scalar_one()

    async def get_lead(self, lead_id: int) -> Lead:
        async for session in self._db.get_session():
            query = (
                select(Lead)
                .options(joinedload(Lead.users))
                .where(Lead.id == lead_id)
            )
            result = await session.execute(query)
        return result.scalars().unique().one()

    async def get_leads(self, limit: int, offset: int) -> list[Lead]:
        async for session in self._db.get_session():
            query = select(Lead).order_by(Lead.created_at).limit(limit).offset(offset)
            result = await session.execute(query)
        return result.scalars().all()

    async def get_count_leads(self) -> int:
        async for session in self._db.get_session():
            query = select(func.count()).select_from(Lead)
            result = await session.execute(query)
        return result.scalar_one()

    async def get_count_paid_users_of_lead(self, lead_id: int) -> int:
        async for session in self._db.get_session():
            query = (
                select(func.count())
                .select_from(Lead)
                .join(LeadUser, LeadUser.lead_id == Lead.id)
                .join(User, User.id == LeadUser.user_id)
                .join(Subscription, Subscription.user_id == User.id)
                .join(Tariff, Tariff.id == Subscription.tariff_id)
                .where(
                    Lead.id == lead_id,
                    Tariff.is_trial.is_(False),
                )
            )
            result = await session.execute(query)
        return result.scalar_one()

    async def get_count_trial_users_of_lead(self, lead_id: int) -> int:
        async for session in self._db.get_session():
            query = (
                select(func.count())
                .select_from(Lead)
                .join(LeadUser, LeadUser.lead_id == Lead.id)
                .join(User, User.id == LeadUser.user_id)
                .join(Subscription, Subscription.user_id == User.id)
                .join(Tariff, Tariff.id == Subscription.tariff_id)
                .where(
                    Lead.id == lead_id,
                    Tariff.is_trial.is_(True),
                )
            )
            result = await session.execute(query)
        return result.scalar_one()

    async def create_lead(self, title: str, url: str, description: str | None = None) -> None:
        async for session in self._db.get_session():
            instance = Lead(
                title=title,
                url=url,
                description=description,
            )
            session.add(instance)
            await session.commit()
