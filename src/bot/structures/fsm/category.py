from aiogram.fsm.state import StatesGroup, State


class CategoryGroup(StatesGroup):
    price = State()
    confirm = State()


class CashbackHistoryGroup(StatesGroup):
    step1 = State()


class SettingsGroup(StatesGroup):
    option = State()
    name = State()
    region = State()


class FeedbackGroup(StatesGroup):
    message = State()
