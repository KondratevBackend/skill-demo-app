from aiogram import types

from src.bot.admin.start.keyboards import start_admin_keyboard


class StartAdminService:
    async def start(self, message: types.Message):
        await message.answer(
            f"<b>Добро пожаловать в админ панель!</b>",
            reply_markup=start_admin_keyboard,
            parse_mode="html",
        )
