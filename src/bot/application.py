import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from src.bot.register_handlers import RegisterHandlers
from src.bot.storage import memory
from src.core import database
from src.core.config import BotConfig

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        db: database.Database,
        config: BotConfig,
        register_handlers: RegisterHandlers,
    ):
        self._db = db
        self._config = config
        self._register_handlers = register_handlers
        self._dp = None
        self._bot = None

    @property
    def bot(self):
        if self._bot is not None:
            return self._bot
        self._bot = Bot(token=self._config.bot.token)
        return self._bot

    @property
    def dp(self):
        if self._dp is not None:
            return self._dp
        main_loop = asyncio.get_event_loop()
        self._dp = Dispatcher(storage=memory, loop=main_loop)
        self._dp.startup.register(self.on_startup)
        self._dp.shutdown.register(self.on_shutdown)
        self._register_handlers.set(dp=self._dp, bot=self._bot)
        return self._dp

    async def on_startup(self):
        await self.set_commands()
        logger.debug("Telegram bot started")

    async def on_shutdown(self):
        await self._bot.session.close()
        logger.debug("Telegram bot stopped")

    async def set_commands(self):
        commands = [
            types.BotCommand(command="start", description="Начать работу с ботом"),
        ]
        await self._bot.set_my_commands(commands)
