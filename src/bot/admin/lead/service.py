from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.admin.lead.dao import LeadAdminDAO
from src.bot.admin.lead.fsm import CreateLeadFSM
from src.bot.admin.lead.keyboards import LeadAdminKeyboard
from src.bot.stop_fsm.keyboards import stop_keyboard
from src.core.config import BotConfig


class LeadAdminService:
    def __init__(self, dao: LeadAdminDAO, keyboard: LeadAdminKeyboard, config: BotConfig):
        self._dao = dao
        self._keyboard = keyboard
        self._config = config

    async def get_title_for_lead(self, callback: types.CallbackQuery, state: FSMContext):
        await state.set_state(CreateLeadFSM.get_title)
        await callback.message.edit_text("Введи название рекламодателя: ")

    async def get_description_for_lead(self, message: types.Message, state: FSMContext):
        if len(message.text) > 64:
            await message.answer(
                f"Длина названия не может превышать 64 символа у тебя {len(message.text)}\n\n" f"Введи название: ",
                reply_markup=stop_keyboard,
            )
            return

        await state.update_data(title=message.text)
        await state.set_state(CreateLeadFSM.get_description)
        await message.answer(
            "Введи описание рекламодателя:\n\n" "copy: <code>Отсутствует</code>",
            parse_mode="html",
        )

    async def get_url_code_for_lead(self, message: types.Message, state: FSMContext):
        if len(message.text) > 1024:
            await message.answer(
                f"Длина описания не может превышать 1024 символа у тебя {len(message.text)}!\n\n" f"Введи описание: ",
                reply_markup=stop_keyboard,
            )
            return

        await state.update_data(description=message.text)
        await state.set_state(CreateLeadFSM.get_url_code)
        await message.answer("Введи код URL-а рекламодателя: ")

    async def create_lead(self, message: types.Message, state: FSMContext):
        url_code = message.text
        if len(url_code) > 32:
            await message.answer(
                f"Длина URL-а не может превышать 32 символа у тебя {len(message.text)}!\n\n" f"Введи код URL-а: ",
                reply_markup=stop_keyboard,
            )
            return
        elif not url_code.isascii() or not url_code.isalpha():
            await message.answer(
                f"URL код может содержать только латиницу!\n\n" f"Введи код URL-а: ",
                reply_markup=stop_keyboard,
            )
            return

        data = await state.get_data()
        title = data.get("title")
        description = data.get("description", "Отсутствует")
        url = f"https://t.me/{self._config.bot.username_bot}?start={url_code}"

        if await self._dao.exists_lead(url=url):
            await message.answer(f"Такая ссылка уже существует!\n" f"URL: {url}\n\n" f"Введи код URL-а: ")
            return

        await self._dao.create_lead(title=title, description=description, url=url)

        await state.clear()
        await message.answer(
            f"<b>Рекламодатель создан</b>\n\n" f"Название: {title}\n" f"Описание: {description}\n" f"URL: {url}",
            parse_mode="html",
        )

    async def get_list_leads(self, callback: types.CallbackQuery):
        pagination_data = callback.data.split("_")[-1].split(":")
        limit = int(pagination_data[0])
        offset = int(pagination_data[1])

        await callback.message.edit_text(
            "Список рекламодателей: ",
            parse_mode="html",
            reply_markup=await self._keyboard.list_leads_keyboard(limit=limit, offset=offset),
        )

    async def get_lead(self, callback: types.CallbackQuery):
        await callback.answer("Ищу рекламодателя...")
        lead_id = int(callback.data.split("_")[-1])

        lead = await self._dao.get_lead(lead_id=lead_id)

        await callback.message.answer(
            f"<b>Рекламодатель</b> {lead.created_at.strftime('%d.%m.%Y')}\n\n"
            f"<b>Название</b>: {lead.title}\n"
            f"<b>Описание</b>: {lead.description}\n"
            f"<b>URL</b>: {lead.url}\n"
            f"{'-'*50}\n"
            f"<b>Статистика</b>\n\n"
            f"<b>Старт</b>: {len(lead.users)}\n"
            f"<b>Пробных</b>: {await self._dao.get_count_trial_users_of_lead(lead_id=lead_id)}\n"
            f"<b>Платных</b>: {await self._dao.get_count_paid_users_of_lead(lead_id=lead_id)}\n",
            parse_mode="html",
        )
