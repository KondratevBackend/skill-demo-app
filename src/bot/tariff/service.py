from aiogram import types

from src.bot.subscription.service import SubscriptionService
from src.bot.tariff.dao import BotTariffDAO
from src.core.payment.service import PaymentService
from src.core.server.service import ServerService
from src.core.tariff.service import TariffService


class BotTariffService:
    def __init__(
        self,
        dao: BotTariffDAO,
        tariff_service: TariffService,
        server_service: ServerService,
        subscription_service: SubscriptionService,
        payment_service: PaymentService,
    ):
        self._dao = dao
        self._tariff_service = tariff_service
        self._server_service = server_service
        self._subscription_service = subscription_service
        self._payment_service = payment_service

    async def give_trial_tariff(self, callback: types.CallbackQuery):
        await callback.answer("Активируем пробный тариф")

        user = await self._dao.get_user(telegram_id=callback.from_user.id)
        if not user.server_id and not await self._dao.exists_available_server():
            await callback.message.answer(
                "Сейчас наблюдается высокая нагрузка — <b>все серверы временно переполнены</b>\n\n"
                "Команда уже занимается этим вопросом 💪\n\n"
                "С любовью Приватка ❤️",
                parse_mode="html",
            )
            return

        if await self._dao.exists_sub(user_id=user.id):
            await callback.message.answer(
                "Раннее ты уже оформлял подписку, поэтому пробный период недоступен\n\n"
                "Но есть классная альтернатива 😉\n"
                "Приглашай друзей по реферальной программе и получай <b>бесплатные</b> дни подписки 🎁",
                parse_mode="html",
                # todo: referral keyboard + maybe support
            )
            return

        tariff_id = int(callback.data.split("trial_tariff_select_")[-1])
        tariff = await self._dao.get_tariff(tariff_id=tariff_id)

        await self._tariff_service.issue_tariff(user=user, tariff=tariff)

        await callback.message.answer("🎉")
        await callback.message.answer(
            f"<b>Ура! Пробный тариф успешно подключен</b> 🔥\n\n"
            f"Тестируй сервис <b>{tariff.days}</b> дня и подключай до <b>{tariff.limit_ip} устройств</b> 🖥️📱💻\n\n"
            f"Пробуй все функции, оцени удобство, и не стесняйся спрашивать поддержку, если появятся вопросы",
            parse_mode="html",
        )
        await self._subscription_service.send_link_to_connection(
            message=callback.message,
            user=user,
        )

    async def buy_tariff(self, callback: types.CallbackQuery):
        await callback.answer("Формируем платеж")

        tariff_id = int(callback.data.split("tariff_select_")[-1])
        tariff = await self._dao.get_tariff(tariff_id=tariff_id)
        await self._payment_service.create_payment_yookassa(price=tariff.price, description=tariff.text)
        await callback.message.answer("Hello paid")
