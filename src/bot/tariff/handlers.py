from aiogram import Dispatcher, F, types

from src.bot.tariff.service import BotTariffService


class BotTariffHandlers:
    def __init__(self, service: BotTariffService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.callback_query(F.data.startswith("trial_tariff_select_"))
        async def trial_tariff_handler(callback: types.CallbackQuery):
            await self._service.give_trial_tariff(callback=callback)

        @dp.callback_query(F.data.startswith("tariff_select_"))
        async def buy_tariff_handler(callback: types.CallbackQuery):
            await self._service.buy_tariff(callback=callback)
