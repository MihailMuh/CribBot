from aiogram.dispatcher.filters.state import State, StatesGroup


class UploadStates(StatesGroup):
    check_key: State = State()
    ticket_number: State = State()
    upload_photo: State = State()
    rate_photos: State = State()
