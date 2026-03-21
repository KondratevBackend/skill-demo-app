from src.core.database.dao import BaseDAO
from src.core.database.models import Payment, PaymentProviderType
from src.core.payment.yookassa.dto import PaymentYookassaDTO


class PaymentDAO(BaseDAO):
    async def create_payment_yookassa(self, payment: PaymentYookassaDTO) -> None:
        async for session in self._db.get_session():
            instance = Payment(
                amount=payment.amount.value,
                currency=payment.amount.currency,
                provider=PaymentProviderType.yookassa,
                provider_payment_id=payment.id,
                status=payment.status,
                tariff_id=payment.metadata.tariff_id,
                user_id=payment.metadata.user_id,
            )
            session.add(instance)
            await session.commit()
