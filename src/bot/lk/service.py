import datetime

from aiogram import types

from src.bot.lk.dao import LKDAO
from src.bot.lk.dto import HumanizeTimeDTO
from src.bot.lk.utils import humanize_time, get_time_until_expiration
from src.core.database.models import Subscription


class LKService:
    def __init__(self, dao: LKDAO):
        self._dao = dao

    async def get_lk(self, message: types.Message):
        user = await self._dao.get_user(telegram_id=message.from_user.id)
        subscription = await self._dao.get_active_subscription(user_id=user.id)

        msg_text = (
            f"<b>Личный кабинет</b> 🔒\n\n"
            f"<b>Ваш телеграм ID:</b> {message.from_user.id}\n\n"
            f"Нет активной подписки 📵"
        )

        if subscription:
            total_subscriptions_duration = await self.get_total_subscriptions_duration(user_id=user.id)

            msg_text = (
                f"<b>Личный кабинет</b> 🔓\n\n"
                f"<b>Телеграм ID:</b> {message.from_user.id}\n\n"
                # TODO: Referral statistic
                f"<b>Текущая подписка:</b> {subscription.tariff.text}\n\n"
                f"<b>До истечения подписки осталось:</b>\n"
                f"<code>{total_subscriptions_duration.show()}</code>"
            )

        await message.answer(
            text=msg_text,
            parse_mode="html"
        )

    async def get_total_subscriptions_duration(
        self,
        user_id: int,
        active_subscription: Subscription | None = None,
    ) -> HumanizeTimeDTO:
        pending_subscriptions: list[Subscription] = await self._dao.get_pending_subscription(user_id=user_id)
        if not active_subscription:
            active_subscription: Subscription = await self._dao.get_active_subscription(user_id=user_id)

        date_of_expiration = active_subscription.expires_at

        for sub in pending_subscriptions:
            date_of_expiration += datetime.timedelta(days=sub.tariff.days)

        time_until_expiration = get_time_until_expiration(date_of_expiration=date_of_expiration)
        return humanize_time(time_dto=time_until_expiration)
