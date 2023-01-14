import shutil
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.controllers.photo_controllers.uploader.photo_uploader_controller import get_photo
from src.core.core import dispatcher


def delete_photos(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


@dispatcher.callback_query_handler(state="*", text="cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    if data := await state.get_data():
        delete_photos(get_photo(data, 666).parent)

    await call.message.answer("Операция отменена")
    await state.finish()
