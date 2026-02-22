from aiogram import Bot, Dispatcher

from src.bot.start.handlers import StartHandlers
from src.bot.tariff.handlers import BotTariffHandlers


class RegisterHandlers:
    def __init__(
        self,
        start_handlers: StartHandlers,
        tariff_handlers: BotTariffHandlers,
    ):
        self._start_handlers = start_handlers
        self._tariff_handlers = tariff_handlers

    def set(self, dp: Dispatcher, bot: Bot):
        self._start_handlers.register_handlers(dp)
        self._tariff_handlers.register_handlers(dp)
