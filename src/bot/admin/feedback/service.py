from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.admin.feedback.dao import FeedbackAdminDAO
from src.bot.admin.feedback.fsm import CreateFeedbackFSM
from src.bot.admin.feedback.keyboards import create_feedback_skip_keyboard, is_verified_user_in_feedback_keyboard


class FeedbackAdminService:
    def __init__(self, dao: FeedbackAdminDAO):
        self._dao = dao

    async def get_user_name_for_feedback(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CreateFeedbackFSM.get_user_name)
        await callback.message.edit_text(
            f"Введи имя пользователя: ",
            parse_mode="html",
            reply_markup=create_feedback_skip_keyboard,
        )

    async def is_verified_user_for_feedback(
        self,
        message: types.Message,
        state: FSMContext,
        skip_user_name: bool = False,
    ):
        if skip_user_name:
            await state.update_data(user_name=None)
        else:
            await state.update_data(user_name=message.text)
        await state.set_state(CreateFeedbackFSM.is_verified_user)

        await message.answer(
            "Пользователь верифицирован?",
            parse_mode="html",
            reply_markup=is_verified_user_in_feedback_keyboard,
        )

    async def get_comment_for_feedback(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.answer()

        is_verified_user: bool = True if callback.data.split(":")[-1] == "true" else False
        await state.update_data(is_verified_user=is_verified_user)
        await state.set_state(CreateFeedbackFSM.get_comment)

        await callback.message.answer(
            "Напиши комментарий к отзыву: ",
            parse_mode="html",
            reply_markup=create_feedback_skip_keyboard,
        )

    async def get_advantages_for_feedback(
        self,
        message: types.Message,
        state: FSMContext,
        skip_comment: bool = False,
    ):
        if skip_comment:
            await state.update_data(comment=None)
        else:
            await state.update_data(comment=message.text)
        await state.set_state(CreateFeedbackFSM.get_advantages)

        await message.answer(
            "Напиши достоинства сервиса: ",
            parse_mode="html",
            reply_markup=create_feedback_skip_keyboard,
        )

    async def get_flaws_for_feedback(
        self,
        message: types.Message,
        state: FSMContext,
        skip_advantages: bool = False,
    ):
        if skip_advantages:
            await state.update_data(advantages=None)
        else:
            await state.update_data(advantages=message.text)
        await state.set_state(CreateFeedbackFSM.get_flaws)

        await message.answer(
            "Напиши недостатки сервиса: ",
            parse_mode="html",
            reply_markup=create_feedback_skip_keyboard,
        )

    async def get_rating_for_feedback(
        self,
        message: types.Message,
        state: FSMContext,
        skip_flaws: bool = False,
    ):
        if skip_flaws:
            await state.update_data(flaws=None)
        else:
            await state.update_data(flaws=message.text)
        await state.set_state(CreateFeedbackFSM.get_rating)

        await message.answer(
            "Оценка (от 1 до 5): ",
            parse_mode="html",
            reply_markup=create_feedback_skip_keyboard,
        )

    async def create_feedback(self, message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            await message.answer(
                "Оценка должна быть строго целым числом\n\n"
                "Введи оценку (от 1 до 5): "
            )
            return

        rating = int(message.text)
        if 0 >= rating > 5:
            await message.answer(
                "Оценка должна быть от 1 до 5\n\n"
                "Введи оценку (от 1 до 5): "
            )
            return

        state_data = await state.get_data()
        await state.clear()

        feedback = await self._dao.create_feedback(
            rating=rating,
            user_name=state_data.get("user_name", None),
            is_verified_user=state_data.get("is_verified_user", False),
            advantages=state_data.get("advantages", None),
            flaws=state_data.get("flaws", None),
            comment=state_data.get("comment", None),
        )

        name_msg = feedback.user_name if feedback.user_name else "Покупатель Приватка-VPN"
        rating_msg = feedback.rating * "⭐️"
        verified_msg = "✅" if feedback.is_verified_user else ""
        advantages_msg = f"\n<i>Достоинства</i>: {feedback.advantages}" if feedback.advantages else ""
        flaws_msg = f"\n<i>Недостатки</i>: {feedback.flaws}" if feedback.flaws else ""
        comment_msg = f"\n<i>Комментарий</i>: {feedback.comment}" if feedback.comment else ""

        await message.answer(
            f"<b>Отзыв успешно создан!</b>\n\n"
            f"```\n"
            f"{name_msg}{verified_msg}  {rating_msg}\n"
            f"{advantages_msg}"
            f"{flaws_msg}"
            f"{comment_msg}"
            f"\n```",
            parse_mode="html"
        )


