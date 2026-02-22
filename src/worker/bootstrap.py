import punq

from src.core.config import WorkerConfig
from src.core.database import Database


def resolve_resources(config: WorkerConfig) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )

    return container
