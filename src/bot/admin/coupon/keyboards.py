from aiogram import types

from src.bot.admin.coupon.dao import CouponAdminDAO


class CouponAdminKeyboards:
    def __init__(self, dao: CouponAdminDAO):
        self._dao = dao

    async def tariffs_keyboard(self):
        tariffs = await self._dao.get_tariffs()

        inline_keyboard: list = [
            [types.InlineKeyboardButton(text=tariff.text, callback_data=f"admin_create_coupon:{tariff.id}")]
            for tariff in tariffs
        ]

        return types.InlineKeyboardMarkup(row_width=1, inline_keyboard=inline_keyboard)

    def create_another_coupon_keyboard(self):
        return types.InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Создать ещё купон", callback_data=f"admin_create_coupon")]
            ],
        )
