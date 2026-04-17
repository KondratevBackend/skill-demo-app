from aiogram import types

from src.bot.feedback.dao import FeedbackDAO
from src.bot.feedback.keyboards import feedback_keyboard
from src.bot.support.keyboards import SupportKeyboards
from src.core.redis import Redis


class FeedbackService:
    def __init__(self, dao: FeedbackDAO, support_keyboards: SupportKeyboards, redis: Redis):
        self._dao = dao
        self._support_keyboards = support_keyboards
        self._redis = redis

    async def msg_how_leave_review(self, message: types.Message):
        await message.answer(
            "<b>Делись своим опытом — нам важен каждый отзыв</b>\n\n"
            "Чтобы оставить отзыв, напиши в поддержку по кнопке ниже <tg-emoji emoji-id='5406745015365943482'>⬇️</tg-emoji>\n\n"
            "Отзывы с отметкой <tg-emoji emoji-id='5206607081334906820'>✔️</tg-emoji> оставлены верифицированными пользователями\n\n"
            "Мы не редактируем отзывы и публикуем их как есть. Отзыв можно оставить анонимно",
            parse_mode="html",
            reply_markup=self._support_keyboards.support_keyboard(),
        )

    async def get_feedback(self, message: types.Message, edit_text: bool = False):
        feedback = await self._dao.get_random_feedback()

        name_msg = feedback.user_name if feedback.user_name else "Покупатель Приватка-VPN"
        rating_msg = feedback.rating * "<tg-emoji emoji-id='5438496463044752972'>⭐️</tg-emoji>"
        verified_msg = "<tg-emoji emoji-id='5206607081334906820'>✔️</tg-emoji>" if feedback.is_verified_user else ""
        advantages_msg = f"\n<i>Достоинства</i>: {feedback.advantages}" if feedback.advantages else ""
        flaws_msg = f"\n<i>Недостатки</i>: {feedback.flaws}" if feedback.flaws else ""
        comment_msg = f"\n<i>Комментарий</i>: {feedback.comment}" if feedback.comment else ""

        text_msg = (
            f"{name_msg}{verified_msg}  {rating_msg}\n"
            f"{advantages_msg}"
            f"{flaws_msg}"
            f"{comment_msg}"
        )

        if edit_text:
            await message.edit_text(
                text=text_msg,
                parse_mode="html",
                reply_markup=feedback_keyboard,
            )
        else:
            await message.answer(
                text=text_msg,
                parse_mode="html",
                reply_markup=feedback_keyboard,
            )

