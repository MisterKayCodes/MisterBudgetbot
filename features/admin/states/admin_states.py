from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_trial_duration = State()
