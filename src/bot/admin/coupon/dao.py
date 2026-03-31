from sqlalchemy import select

from src.core.database.dao import BaseDAO
from src.core.database.models import Coupon, Tariff


class CouponAdminDAO(BaseDAO):
    async def get_tariffs(self) -> list[Tariff]:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).order_by(Tariff.order_index))
        return result.scalars().all()

    async def get_tariff(self, tariff_id: int) -> Tariff:
        async for session in self._db.get_session():
            result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        return result.scalar_one()

    async def create_coupon(self, code: str, tariff_id: int) -> Coupon:
        async for session in self._db.get_session():
            instance = Coupon(
                code=code,
                tariff_id=tariff_id,
            )
            session.add(instance)
            await session.commit()

        return instance
