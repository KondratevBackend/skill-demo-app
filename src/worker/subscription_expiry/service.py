import asyncio

from src.bot import bot
from src.core.database.models import Subscription
from src.core.server.service import ServerService
from src.worker.subscription_expiry.dao import SubscriptionExpiryWorkerDAO


class SubscriptionExpiryWorkerService:
    def __init__(self, dao: SubscriptionExpiryWorkerDAO, server_service: ServerService):
        self._dao = dao
        self._server_service = server_service

    async def process(self):
        subscriptions = await self._dao.get_subscriptions_with_expire_data_and_active()
        await asyncio.gather(
            *[self._switching_subscription(subscription=subscription) for subscription in subscriptions]
        )

    async def _switching_subscription(self, subscription: Subscription):
        await self._dao.deactivate_subscription(subscription_id=subscription.id)

        next_subscription = await self._dao.get_earliest_pending_subscription(subscription.user_id)
        if next_subscription:
            await self._dao.activate_subscription(subscription_id=next_subscription.id)
        else:
            user = await self._dao.get_user(user_id=subscription.user_id)
            await self._server_service.disable_user(user=user)
            await bot.send_message(
                chat_id=user.telegram_id,
                text="Тариф истек и ты был отключен от сервера :(",
                parse_mode="html",
                # todo: keyboard tariffs
            )
