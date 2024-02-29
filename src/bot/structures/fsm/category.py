from aiogram.fsm.state import StatesGroup, State


class CategoryGroup(StatesGroup):
    price = State()
    confirm = State()