import uuid

from src.core.config import YookassaSettings
from src.core.payment.yookassa.api import YookassaAPI
from src.core.payment.yookassa.dto import PaymentYookassaPayloadDTO


class PaymentService:
    def __init__(self, yookassa_api: YookassaAPI, config: YookassaSettings):
        self._yookassa_api = yookassa_api
        self._config = config

    async def create_payment_yookassa(
        self,
        price: float,
        description: str | None = None,
    ):
        idempotency_key = uuid.uuid4()
        payload = PaymentYookassaPayloadDTO(
            amount={"value": price},
            description=description,
            confirmation={"return_url": self._config.success_url}
        )
        response = await self._yookassa_api.create_payment(payload=payload, idempotency_key=idempotency_key)
        print(response)
