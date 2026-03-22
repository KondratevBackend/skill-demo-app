from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from src.bot.admin.filters import IsAdminFilter
from src.bot.admin.lead.fsm import CreateLeadFSM
from src.bot.admin.lead.service import LeadAdminService


class LeadAdminHandlers:
    def __init__(self, service: LeadAdminService, is_admin_filter: IsAdminFilter):
        self._service = service
        self._is_admin_filter = is_admin_filter

    def register_handlers(self, dp: Dispatcher):
        @dp.callback_query(self._is_admin_filter, F.data == "admin_create_lead")
        async def get_title_for_lead_handler(callback: types.CallbackQuery, state: FSMContext):
            await self._service.get_title_for_lead(callback=callback, state=state)

        @dp.message(self._is_admin_filter, CreateLeadFSM.get_title)
        async def get_description_for_lead_handler(message: types.Message, state: FSMContext):
            await self._service.get_description_for_lead(message=message, state=state)

        @dp.message(self._is_admin_filter, CreateLeadFSM.get_description)
        async def get_url_code_for_lead_handler(message: types.Message, state: FSMContext):
            await self._service.get_url_code_for_lead(message=message, state=state)

        @dp.message(self._is_admin_filter, CreateLeadFSM.get_url_code)
        async def create_lead_handler(message: types.Message, state: FSMContext):
            await self._service.create_lead(message=message, state=state)

        @dp.callback_query(self._is_admin_filter, F.data == "admin_list_lead")
        async def list_lead_handler(callback: types.CallbackQuery):
            pass
