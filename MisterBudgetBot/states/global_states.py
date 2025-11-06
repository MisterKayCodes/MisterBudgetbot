from aiogram.fsm.state import State, StatesGroup

class OnboardingStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()

class MenuStates(StatesGroup):
    main_menu = State()
