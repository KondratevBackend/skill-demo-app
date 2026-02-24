from aiogram import types

from src.bot.subscription.dao import SubscriptionDAO
from src.bot.subscription.keyboards import instruction_keyboard
from src.core.database.models import User
from src.core.server.service import ServerService


class SubscriptionService:
    def __init__(self, dao: SubscriptionDAO, server_service: ServerService):
        self._dao = dao
        self._server_service = server_service

    async def get_connection_link(self, user: User) -> str:
        server = await self._dao.get_server(server_id=user.server_id)
        return f"{await self._server_service.get_sub_uri(server=server)}{user.xui_sub_id}"

    async def send_link_to_connection(self, message: types.Message, user: User) -> None:
        connection_link = await self.get_connection_link(user=user)
        await message.answer(
            text=f"<code>{connection_link}</code>",
            parse_mode="html",
            reply_markup=instruction_keyboard
        )
