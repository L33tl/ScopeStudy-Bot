from aiogram.filters.state import StatesGroup, State


class LocationStates(StatesGroup):
    UNKNOWN_LOCATION = State()
    CHANGE_LOCATION = State()
    HAVE_LOCATION = State()
