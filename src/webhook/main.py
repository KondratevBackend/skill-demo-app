import punq

from src.core.config import WebhookConfig as Config
from src.webhook import application
from src.webhook.bootstrap import resolve_resources

config = Config()
resources = resolve_resources(config=config)
resources.register(service=application.Application, factory=application.Application, scope=punq.Scope.singleton)
app = resources.resolve(service_key=application.Application).app
