import fastapi
import sqlalchemy

from src.core.database import Database


class HealthChecksRouter:
    def __init__(self, db: Database):
        self._db = db

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/health", tags=["Health Checks API"])
        self._include_routes(router=router)
        return router

    def _include_routes(self, router: fastapi.APIRouter) -> None:
        @router.get("/ping")
        async def get_ping():
            return "pong"

        @router.get(
            "/ready",
            responses={
                500: {"description": "Database connection error"},
            },
        )
        async def get_ready():
            try:
                async for session in self._db.get_session():
                    await session.execute(sqlalchemy.text("SELECT version()"))
                return "ready"
            except sqlalchemy.exc.SQLAlchemyError as e:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database connection error",
                ) from e
