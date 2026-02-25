from aiogram.fsm.state import State, StatesGroup


class CouponFSM(StatesGroup):
    get_code = State()
