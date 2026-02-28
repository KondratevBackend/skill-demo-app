import punq

from src.core.config import WebhookConfig
from src.core.database import Database
from src.core.server.cookie.dao import ServerCookieDAO
from src.core.server.cookie.service import ServerCookieService
from src.core.server.dao import ServerDAO
from src.core.server.service import ServerService
from src.core.tariff.dao import TariffDAO
from src.core.tariff.service import TariffService
from src.webhook.health_checks.router import HealthChecksRouter
from src.webhook.yookassa.dao import YookassaDAO
from src.webhook.yookassa.router import YookassaRouter
from src.webhook.yookassa.service import YookassaService


def resolve_resources(config: WebhookConfig) -> punq.Container:
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
        service=TariffDAO,
        factory=TariffDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=TariffService,
        factory=TariffService,
        scope=punq.Scope.singleton,
    )

    container.register(
        service=HealthChecksRouter,
        factory=HealthChecksRouter,
        scope=punq.Scope.singleton,
    )

    register_yookassa(container=container, config=config)

    return container


def register_yookassa(container: punq.Container, config: WebhookConfig) -> None:
    container.register(
        service=YookassaRouter,
        factory=YookassaRouter,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=YookassaService,
        factory=YookassaService,
        scope=punq.Scope.singleton,
        config=config,
    )
    container.register(
        service=YookassaDAO,
        factory=YookassaDAO,
        scope=punq.Scope.singleton,
    )
