from contextlib import asynccontextmanager

import fastapi

from src.core.database import Database
from src.webhook import health_checks


class Application:
    def __init__(
        self,
        health_checks_router: health_checks.router.HealthChecksRouter,
        db: Database,
    ):
        self._db = db
        self._health_checks_router = health_checks_router
        self._app = None

    @property
    def app(self) -> fastapi.FastAPI:
        if self._app is not None:
            return self._app

        @asynccontextmanager
        async def lifespan(app: fastapi.FastAPI):  # noqa: ARG001
            yield
            await self._db.shutdown()

        server = fastapi.FastAPI(
            title="Приватка Webhook",
            version="1.0.0",
            lifespan=lifespan,
            root_path="/src",
            openapi_url="/opnapi.json",
        )
        self._set_up(server=server)
        self._app = server

        return server

    def _set_up(self, server: fastapi.FastAPI) -> None:
        server.include_router(self._health_checks_router.router)
