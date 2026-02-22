import logging

from aiogram import Dispatcher
from aiogram.types import Update

from src.core import consts
from src.core.config import BotConfig
from src.core.exceptions import ServersFullError

logger = logging.getLogger(__name__)


class GlobalMiddleware:
    def __init__(self, config: BotConfig):
        self._config = config

    async def errors_middleware(self, handler, event: Update, data: dict):
        bot = data.get("bot")

        try:
            return await handler(event, data)
        except ServersFullError:
            if bot:
                for admin in self._config.bot.admins:
                    await bot.send_message(chat_id=admin, text=consts.NOTIFICATION_SERVER_FULL, parse_mode="html")
            raise
        except Exception as e:
            logger.exception(f"Ошибка при обработке {event}: {e}")
            raise

    def add_middleware(self, dp: Dispatcher):
        dp.update.outer_middleware(self.errors_middleware)
