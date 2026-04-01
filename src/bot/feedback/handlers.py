from aiogram import Dispatcher, F, types

from src.bot.feedback.service import FeedbackService
from src.core.consts import FEEDBACK_BUTTON_TEXT


class FeedbackHandlers:
    def __init__(self, service: FeedbackService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.message(
            F.text.in_(
                [
                    FEEDBACK_BUTTON_TEXT,
                ]
            )
        )
        async def feedback_handler(message: types.Message):
            await self._service.msg_how_leave_review(message=message)
            await self._service.get_feedback(message=message)

        @dp.callback_query(F.data == "feedback_next")
        async def feedback_next_callback_handler(callback: types.CallbackQuery):
            await self._service.get_feedback(message=callback.message, edit_text=True)
