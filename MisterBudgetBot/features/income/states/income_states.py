from aiogram.fsm.state import State, StatesGroup

class IncomeStates(StatesGroup):
    waiting_for_amount = State()
    viewing_recent = State()
