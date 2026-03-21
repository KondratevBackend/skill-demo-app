import logging
import uuid

from src.core.config import YookassaSettings
from src.core.database.models import Tariff
from src.core.payment.dao import PaymentDAO
from src.core.payment.yookassa.api import YookassaAPI
from src.core.payment.yookassa.dto import PaymentYookassaPayloadDTO, PaymentYookassaDTO

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, yookassa_api: YookassaAPI, dao: PaymentDAO, config: YookassaSettings):
        self._yookassa_api = yookassa_api
        self._dao = dao
        self._config = config

    async def create_payment_yookassa(
        self,
        tariff: Tariff,
        user_id: int,
        description: str | None = None,
    ) -> PaymentYookassaDTO:
        idempotency_key = uuid.uuid4()
        payload = PaymentYookassaPayloadDTO(
            amount={"value": tariff.price},
            description=description or tariff.text,
            confirmation={"type": "redirect", "return_url": self._config.success_url},
            metadata={
                "tariff_id": tariff.id,
                "user_id": user_id,
            }
        )
        payment = await self._yookassa_api.create_payment(payload=payload, idempotency_key=idempotency_key)

        logger.debug(f"Created payment yookassa for {user_id=}")

        return payment
