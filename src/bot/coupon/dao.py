from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from src.core.database.dao import BaseDAO
from src.core.database.models import Coupon, User


class CouponDAO(BaseDAO):
    async def get_user(self, telegram_id: int) -> User:
        async for session in self._db.get_session():
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
        return result.scalar_one()

    async def get_coupon(self, code: str) -> Coupon:
        async for session in self._db.get_session():
            query = select(Coupon).options(joinedload(Coupon.tariff)).where(Coupon.code == code)
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def delete_coupon(self, coupon_id: int) -> None:
        async for session in self._db.get_session():
            query = delete(Coupon).where(Coupon.id == coupon_id)
            await session.execute(query)
            await session.commit()
