from aiogram.fsm.state import State, StatesGroup

class SettingsStates(StatesGroup):
    waiting_for_spending_percent = State()
    waiting_for_savings_percent = State()
    waiting_for_business_percent = State()
