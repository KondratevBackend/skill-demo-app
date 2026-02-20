import punq
from aiogram import Bot, Dispatcher

from src.bot.application import Application
from src.bot.bootstrap import resolve_resources
from src.core.config import BotConfig as Config

config = Config()
container: punq.Container = resolve_resources(config=config)
container.register(service=Application, factory=Application, scope=punq.Scope.singleton, config=config)
application = container.resolve(service_key=Application)
bot: Bot = application.bot
dp: Dispatcher = application.dp
