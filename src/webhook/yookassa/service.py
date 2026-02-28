from src.core.config import WebhookConfig
from src.webhook.yookassa.dao import YookassaDAO


class YookassaService:
    def __init__(self, dao: YookassaDAO, config: WebhookConfig):
        self._dao = dao
        self._config = config

    async def process(self):
        pass
