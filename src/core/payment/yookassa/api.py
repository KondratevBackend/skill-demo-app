import uuid

from aiohttp import helpers

from src.core.api import API
from src.core.config import YookassaSettings
from src.core.payment.yookassa.dto import PaymentYookassaDTO, PaymentYookassaPayloadDTO


class YookassaAPI(API):
    def __init__(self, config: YookassaSettings):
        super().__init__(config=config)
        self.__shop_id = config.shop_id
        self.__secret_key = config.secret_key
        self._headers = self.prepare_request_headers

    @property
    def prepare_request_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": helpers.BasicAuth(str(self.__shop_id), self.__secret_key).encode(),
            **self.default_headers,
        }

    async def create_payment(
        self, payload: PaymentYookassaPayloadDTO, idempotency_key: uuid.UUID
    ) -> PaymentYookassaDTO:
        url = f"payments"
        payload_dict: dict = payload.model_dump()
        self._headers.update({"Idempotence-Key": str(idempotency_key)})

        response = await self._session.post(url, json=payload_dict, headers=self._headers)
        if response.ok:
            result = await response.json()
            print(result)
            return PaymentYookassaDTO(**result)

        response.raise_for_status()
