from aiogram.fsm.state import State, StatesGroup

class StartStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()

class IncomeStates(StatesGroup):
    waiting_for_amount = State()

class ExpenseStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_amount = State()

class GoalsStates(StatesGroup):
    waiting_for_goal_name = State()
    waiting_for_target_amount = State()
    waiting_for_deadline = State()
    waiting_for_auto_save_percent = State()

class SettingsStates(StatesGroup):
    waiting_for_spending_percent = State()
    waiting_for_savings_percent = State()
