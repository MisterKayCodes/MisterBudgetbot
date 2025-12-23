from aiogram.fsm.state import State, StatesGroup

class GoalsStates(StatesGroup):
    waiting_for_goal_name = State()
    waiting_for_target_amount = State()
    waiting_for_deadline = State()
    waiting_for_auto_save_percent = State()
