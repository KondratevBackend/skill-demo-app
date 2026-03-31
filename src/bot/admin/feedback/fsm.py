from aiogram.fsm.state import StatesGroup, State


class CreateFeedbackFSM(StatesGroup):
    get_user_name = State()
    is_verified_user = State()
    get_comment = State()
    get_advantages = State()
    get_flaws = State()
    get_rating = State()
