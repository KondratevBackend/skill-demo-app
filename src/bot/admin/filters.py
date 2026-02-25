from aiogram import types
from aiogram.filters import Filter

from src.core.config import BotConfig


class IsAdminFilter(Filter):
    def __init__(self, config: BotConfig):
        self._admins = config.bot.admins

    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        return message.from_user.id in self._admins
