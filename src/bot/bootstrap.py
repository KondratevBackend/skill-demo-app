import punq

from src.bot.register_handlers import RegisterHandlers
from src.bot.start.dao import StartDAO
from src.bot.start.handlers import StartHandlers
from src.bot.start.keyboards import StartKeyboard
from src.bot.start.service import StartService
from src.core.config import BotConfig as Config
from src.core.database import Database


def resolve_resources(config: Config) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=RegisterHandlers,
        factory=RegisterHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartHandlers,
        factory=StartHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartService,
        factory=StartService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartDAO,
        factory=StartDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartKeyboard,
        factory=StartKeyboard,
        scope=punq.Scope.singleton,
    )

    return container
