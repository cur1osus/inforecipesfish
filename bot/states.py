from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    recipe_section_enter_name = State()
    recipe_enter_name = State()
    recipe_enter_text = State()
