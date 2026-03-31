from aiogram import types

from src.bot.admin.coupon.dao import CouponAdminDAO
from src.bot.admin.coupon.keyboards import CouponAdminKeyboards
from src.bot.admin.coupon.utils import generate_coupon_code
from src.core.exceptions import NotFoundError


class CouponAdminService:
    def __init__(self, dao: CouponAdminDAO, keyboard: CouponAdminKeyboards):
        self._dao = dao
        self._keyboard = keyboard

    async def get_tariffs(self, callback: types.CallbackQuery):
        await callback.answer("Формируем запрос")
        await callback.message.answer(
            "Выбери тариф для которого создать купон: ",
            parse_mode="html",
            reply_markup=await self._keyboard.tariffs_keyboard(),
        )

    async def create_coupon(self, callback: types.CallbackQuery):
        await callback.answer("Создаем купон")
        tariff_id = int(callback.data.split(":")[-1])
        tariff = await self._dao.get_tariff(tariff_id=tariff_id)
        if not tariff:
            await callback.message.answer(
                "⚠️<b>WARNING!</b>⚠️\n\n" "Техническая ошибка. Такой тариф не был найден в системе",
                parse_mode="html",
            )
            raise NotFoundError(f"No rate found when generating a coupon (id={tariff_id})")

        code = generate_coupon_code()
        # TODO: Recursively check if similar code already exists in the system
        await self._dao.create_coupon(code=code, tariff_id=tariff.id)
        await callback.message.edit_text(
            f"Сгенерированный купон:\n\n<code>{code}</code>",
            parse_mode="html",
            reply_markup=self._keyboard.create_another_coupon_keyboard(),
        )
