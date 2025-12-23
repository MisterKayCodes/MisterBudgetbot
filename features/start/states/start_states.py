from aiogram.fsm.state import State, StatesGroup

class StartStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()
