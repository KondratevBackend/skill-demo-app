from aiogram import Dispatcher, F, types
from aiogram.fsm.context import FSMContext

from src.bot.admin.feedback.fsm import CreateFeedbackFSM
from src.bot.admin.feedback.service import FeedbackAdminService
from src.bot.admin.filters import IsAdminFilter


class FeedbackAdminHandlers:
    def __init__(self, service: FeedbackAdminService, is_admin_filter: IsAdminFilter):
        self._service = service
        self._is_admin_filter = is_admin_filter

    def register_handlers(self, dp: Dispatcher):
        @dp.callback_query(self._is_admin_filter, F.data == "admin_create_feedback")
        async def get_user_name_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await self._service.get_user_name_for_feedback(callback=callback, state=state)

        @dp.callback_query(
            self._is_admin_filter,
            F.data == "admin_create_feedback_skip",
            CreateFeedbackFSM.get_user_name,
        )
        async def skip_user_name_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer()
            await self._service.is_verified_user_for_feedback(
                message=callback.message,
                state=state,
                skip_user_name=True,
            )

        @dp.message(self._is_admin_filter, CreateFeedbackFSM.get_user_name)
        async def is_verified_user_for_feedback_handler(message: types.Message, state: FSMContext):
            await self._service.is_verified_user_for_feedback(message=message, state=state)

        @dp.callback_query(
            self._is_admin_filter,
            F.data.startswith("admin_create_feedback_verified_user:"),
            CreateFeedbackFSM.is_verified_user,
        )
        async def get_comment_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await self._service.get_comment_for_feedback(callback=callback, state=state)

        @dp.callback_query(
            self._is_admin_filter,
            F.data == "admin_create_feedback_skip",
            CreateFeedbackFSM.get_comment,
        )
        async def skip_comment_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer()
            await self._service.get_advantages_for_feedback(message=callback.message, state=state, skip_comment=True)

        @dp.message(self._is_admin_filter, CreateFeedbackFSM.get_comment)
        async def get_advantages_for_feedback_handler(message: types.Message, state: FSMContext):
            await self._service.get_advantages_for_feedback(message=message, state=state)

        @dp.callback_query(
            self._is_admin_filter,
            F.data == "admin_create_feedback_skip",
            CreateFeedbackFSM.get_advantages,
        )
        async def skip_advantages_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer()
            await self._service.get_flaws_for_feedback(message=callback.message, state=state, skip_advantages=True)

        @dp.message(self._is_admin_filter, CreateFeedbackFSM.get_advantages)
        async def get_flaws_for_feedback_handler(message: types.Message, state: FSMContext):
            await self._service.get_flaws_for_feedback(message=message, state=state)

        @dp.callback_query(
            self._is_admin_filter,
            F.data == "admin_create_feedback_skip",
            CreateFeedbackFSM.get_flaws,
        )
        async def skip_flaws_for_feedback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer()
            await self._service.get_rating_for_feedback(message=callback.message, state=state, skip_flaws=True)

        @dp.message(self._is_admin_filter, CreateFeedbackFSM.get_flaws)
        async def get_rating_for_feedback_handler(message: types.Message, state: FSMContext):
            await self._service.get_rating_for_feedback(message=message, state=state)

        @dp.message(self._is_admin_filter, CreateFeedbackFSM.get_rating)
        async def create_feedback_handler(message: types.Message, state: FSMContext):
            await self._service.create_feedback(message=message, state=state)
