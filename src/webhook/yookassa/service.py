import asyncio
import logging

from src.bot import bot
from src.core.config import WebhookConfig
from src.core.database.models import PaymentStatusType
from src.core.payment.yookassa.dto import PaymentYookassaDTO
from src.core.tariff.service import TariffService
from src.webhook.yookassa.dao import YookassaDAO
from src.webhook.yookassa.dto import WebhookNotificationDTO

logger = logging.getLogger(__name__)


class YookassaService:
    def __init__(self, dao: YookassaDAO, tariff_service: TariffService, config: WebhookConfig):
        self._dao = dao
        self._tariff_service = tariff_service
        self._config = config

    async def process(self, notification: WebhookNotificationDTO) -> bool:
        status_event: PaymentStatusType = self.__parse_event(notification)

        # TODO: exists payment and webhook event????

        if status_event == PaymentStatusType.succeeded:
            await self.handle_event_succeeded(payment=notification.object)
        elif status_event == PaymentStatusType.waiting_for_capture:
            await self.handle_event_waiting_for_capture(payment=notification.object)
        elif status_event == PaymentStatusType.canceled:
            await self.handle_event_canceled(payment=notification.object)
        else:
            logger.warning(f"Unknown payment status: {status_event}")

        return True

    async def handle_event_succeeded(self, payment: PaymentYookassaDTO):
        user, tariff = await asyncio.gather(
            self._dao.get_user(user_id=payment.metadata.user_id),
            self._dao.get_tariff(tariff_id=payment.metadata.tariff_id),
        )
        await asyncio.gather(
            self._tariff_service.issue_tariff(user=user, tariff=tariff),
            self._dao.update_payment_status(status=payment.status, provider_payment_id=payment.id),
        )
        emoji_firework = "<tg-emoji emoji-id='5193018401810822951'>🎉</tg-emoji>"
        success_text = (
            f"Yupiii {emoji_firework * 3}\n"
            f"Тариф {tariff.text} успешно активирован <tg-emoji emoji-id='5197288647275071607'>🛡</tg-emoji>\n\n"
        )
        await bot.send_message(chat_id=user.telegram_id, text=success_text, parse_mode="html")

    async def handle_event_waiting_for_capture(self, payment: PaymentYookassaDTO):
        await self._dao.update_payment_status(status=payment.status, provider_payment_id=payment.id)
        logger.debug(f"Payment {payment.id=} waiting for capture")

    async def handle_event_canceled(self, payment: PaymentYookassaDTO):
        await self._dao.update_payment_status(status=payment.status, provider_payment_id=payment.id)
        logger.debug(f"Payment {payment.id=} canceled")

    @staticmethod
    def __parse_event(notification: WebhookNotificationDTO) -> PaymentStatusType:
        return PaymentStatusType(notification.event.split(".")[-1])
