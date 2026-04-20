from sqlalchemy import select, update, insert

from src.core.database.dao import BaseDAO
from src.core.database.models import Payment, PaymentProviderType, PaymentStatusType, Tariff, User, WebhookEvent
from src.webhook.yookassa.dto import WebhookNotificationDTO


class YookassaDAO(BaseDAO):
    async def get_user(self, user_id: int) -> User:
        async for session in self._db.get_session():
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
        return result.scalar_one()

    async def get_tariff(self, tariff_id: int) -> Tariff:
        async for session in self._db.get_session():
            query = select(Tariff).where(Tariff.id == tariff_id)
            result = await session.execute(query)
        return result.scalar_one()

    async def update_payment_status(self, status: PaymentStatusType, provider_payment_id: str):
        async for session in self._db.get_session():
            query = (
                update(Payment)
                .values(status=status)
                .where(
                    Payment.provider_payment_id == provider_payment_id,
                    Payment.provider == PaymentProviderType.yookassa,
                )
            )
            await session.execute(query)
            await session.commit()

    async def insert_webhook_event(self, notification: WebhookNotificationDTO):
        async for session in self._db.get_session():
            instance = WebhookEvent(
                provider=PaymentProviderType.yookassa,
                provider_event_id=notification.object.id,
                event_type=notification.event,
                payload_json=notification,
            )
            session.add(instance)
            await session.commit()