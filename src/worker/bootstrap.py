import punq

from src.core.config import WorkerConfig
from src.core.database import Database
from src.core.server.cookie.dao import ServerCookieDAO
from src.core.server.cookie.service import ServerCookieService
from src.core.server.dao import ServerDAO
from src.core.server.service import ServerService
from src.worker.subscription_expiry.dao import SubscriptionExpiryWorkerDAO
from src.worker.subscription_expiry.service import SubscriptionExpiryWorkerService


def resolve_resources(config: WorkerConfig) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=ServerService,
        factory=ServerService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=ServerDAO,
        factory=ServerDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=ServerCookieService,
        factory=ServerCookieService,
        scope=punq.Scope.singleton,
        config=config.server,
    )
    container.register(
        service=ServerCookieDAO,
        factory=ServerCookieDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=SubscriptionExpiryWorkerService,
        factory=SubscriptionExpiryWorkerService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=SubscriptionExpiryWorkerDAO,
        factory=SubscriptionExpiryWorkerDAO,
        scope=punq.Scope.singleton,
    )

    return container
