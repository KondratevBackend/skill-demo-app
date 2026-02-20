from aiogram import Bot, Dispatcher

from src.bot.start.handlers import StartHandlers


class RegisterHandlers:
    def __init__(
        self,
        start_handlers: StartHandlers,
    ):
        self.start_handlers = start_handlers

    def set(self, dp: Dispatcher, bot: Bot):
        self.start_handlers.register_handlers(dp)
