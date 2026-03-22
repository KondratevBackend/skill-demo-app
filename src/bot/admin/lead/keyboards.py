from aiogram import types

from src.bot.admin.lead.dao import LeadAdminDAO


class LeadAdminKeyboard:
    def __init__(self, dao: LeadAdminDAO):
        self._dao = dao

    async def list_leads_keyboard(self, limit: int, offset: int) -> types.InlineKeyboardMarkup:
        leads = await self._dao.get_leads(limit=limit, offset=offset)

        inline_keyboard: list = []
        for lead in leads:
            inline_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text=lead.title,
                        callback_data=f"admin_get_lead_{lead.id}",
                    )
                ]
            )

        pagination_keyboard: list = []
        if offset > 0:
            pagination_keyboard.append(
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"admin_list_leads_{limit}:{offset - limit}",
                )
            )
        if offset + limit < await self._dao.get_count_leads():
            pagination_keyboard.append(
                types.InlineKeyboardButton(
                    text="Дальше",
                    callback_data=f"admin_list_leads_{limit}:{offset + limit}",
                )
            )

        if pagination_keyboard:
            inline_keyboard.append(pagination_keyboard)

        return types.InlineKeyboardMarkup(row_width=1, inline_keyboard=inline_keyboard)
