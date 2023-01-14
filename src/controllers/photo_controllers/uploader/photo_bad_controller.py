from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from src.buttons import button_cancel
from src.controllers.photo_controllers.uploader.cancel_controller import delete_photos
from src.controllers.photo_controllers.uploader.photo_uploader_controller import get_photo
from src.controllers.photo_controllers.uploader.upload_state import UploadStates
from src.core.core import dispatcher


@dispatcher.callback_query_handler(state=UploadStates.rate_photos, text="bad")
async def photo_bad(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Тогда жду другие фотки",
                              reply_markup=InlineKeyboardMarkup(row_width=1).add(button_cancel))
    delete_photos(get_photo(await state.get_data(), 666).parent)

    await state.update_data(photos=[])
    await UploadStates.upload_photo.set()
