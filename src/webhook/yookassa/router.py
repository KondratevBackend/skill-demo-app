import json

import fastapi

from src.webhook.yookassa.dto import WebhookNotificationDTO
from src.webhook.yookassa.service import YookassaService


class YookassaRouter:
    def __init__(self, service: YookassaService):
        self._service = service

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/yookassa", tags=["Yookassa Webhook"])
        self._include_routes(router=router)
        return router

    def _include_routes(self, router: fastapi.APIRouter) -> None:
        @router.post(
            path="/process",
            description="Webhook handler",
            status_code=fastapi.status.HTTP_200_OK,
        )
        async def process(notification: WebhookNotificationDTO) -> fastapi.Response:
            ok = await self._service.process(notification=notification)

            if ok:
                return fastapi.status.HTTP_200_OK
