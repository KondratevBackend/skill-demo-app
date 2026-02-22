from aiogram import types

from src.bot.tariff.dao import BotTariffDAO
from src.core.tariff.service import TariffService


class BotTariffService:
    def __init__(self, dao: BotTariffDAO, tariff_service: TariffService):
        self._dao = dao
        self._tariff_service = tariff_service

    async def give_trial_tariff(self, callback: types.CallbackQuery):
        await callback.answer("Активируем пробный тариф")

        user = await self._dao.get_user(telegram_id=callback.from_user.id)
        tariff_id = int(callback.data.split("trial_tariff_select_")[-1])
        tariff = await self._dao.get_tariff(tariff_id=tariff_id)

        await self._tariff_service.issue_tariff(user=user, tariff=tariff)

        await callback.message.answer("Hello")

    async def buy_tariff(self, callback: types.CallbackQuery):
        await callback.answer("Формируем платеж")

        await callback.message.answer("Hello paid")
