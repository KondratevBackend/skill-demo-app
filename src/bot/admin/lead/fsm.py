from aiogram.fsm.state import State, StatesGroup


class CreateLeadFSM(StatesGroup):
    get_title = State()
    get_description = State()
    get_url_code = State()
