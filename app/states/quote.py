from aiogram.fsm.state import State, StatesGroup


class QuoteForm(StatesGroup):
    zone = State()
    idea = State()
    size = State()
    work_type = State()
    references = State()
    contact = State()
    confirm = State()
