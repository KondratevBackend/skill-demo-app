import fastapi

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
        @router.get("/process")
        async def process() -> None:
            await self._service.process()
