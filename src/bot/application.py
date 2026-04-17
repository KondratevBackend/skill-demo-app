import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from src.bot.middlewares import GlobalMiddleware
from src.bot.register_handlers import RegisterHandlers
from src.bot.storage import memory
from src.core import database
from src.core.config import BotConfig
from src.core.payment.yookassa.api import YookassaAPI
from src.core.redis import Redis

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        db: database.Database,
        redis: Redis,
        config: BotConfig,
        middleware: GlobalMiddleware,
        register_handlers: RegisterHandlers,
        yookassa_api: YookassaAPI,
    ):
        self._db = db
        self._redis = redis
        self._config = config
        self._register_handlers = register_handlers
        self._middleware = middleware
        self._yookassa_api = yookassa_api
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
        self._middleware.add_middleware(dp=self._dp)
        self._register_handlers.set(dp=self._dp, bot=self._bot)
        return self._dp

    async def on_startup(self):
        await self.set_commands()
        await self._redis.startup()
        await self._yookassa_api.startup()
        logger.debug("Telegram bot started")

    async def on_shutdown(self):
        await self._bot.session.close()
        await self._redis.shutdown()
        await self._yookassa_api.shutdown()
        logger.debug("Telegram bot stopped")

    async def set_commands(self):
        commands = [
            types.BotCommand(command="start", description="Начать работу с ботом"),
        ]
        await self._bot.set_my_commands(commands)
