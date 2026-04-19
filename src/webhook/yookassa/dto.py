from pydantic import BaseModel

from src.core.payment.yookassa.dto import PaymentYookassaDTO


class WebhookNotificationDTO(BaseModel):
    type: str
    event: str
    object: PaymentYookassaDTO
