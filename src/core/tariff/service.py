from src.core.database.models import SubscriptionStatusType, Tariff, User
from src.core.server.service import ServerService
from src.core.tariff.dao import TariffDAO


class TariffService:
    def __init__(self, dao: TariffDAO, server_service: ServerService):
        self._dao = dao
        self._server_service = server_service

    async def issue_tariff(self, user: User, tariff: Tariff):
        if not await self._dao.exists_sub(user_id=user.id):
            await self._dao.add_sub(
                user_id=user.id,
                tariff=tariff,
                status=SubscriptionStatusType.active,
            )
            await self._server_service.enable_user(user=user)
            return

        await self._dao.add_sub(
            user_id=user.id,
            tariff=tariff,
            status=SubscriptionStatusType.pending,
        )
