from aiogram import types

from src.bot.lk.dao import LKDAO


class LKService:
    def __init__(self, dao: LKDAO):
        self._dao = dao

    async def get_lk(self, message: types.Message):
        await message.answer("Личный кабинет!")
