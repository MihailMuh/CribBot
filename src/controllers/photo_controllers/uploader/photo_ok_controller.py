import shutil
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.constants import BASE_DIR
from src.controllers.photo_controllers.uploader.upload_state import UploadStates
from src.core.core import dispatcher
from src.crib_data import crib_data


@dispatcher.callback_query_handler(state=UploadStates.rate_photos, text="ok")
async def photo_ok(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Решения успешно сохранены")

    data: dict = await state.get_data()
    dest_photo_path: Path = BASE_DIR / "photo" / data["term"] / data["subject"]

    # replace prefix with temp dir in path for crib_data
    new_photos: list = list(map(lambda photo: dest_photo_path / Path(photo).name, data["photos"]))

    # delete old photos
    for photo in crib_data[data["term"]][data["subject"]]["photos"][data["number"]]:
        photo.unlink()

    # set ... 46: [Path("/home/user/.../45_1.jpg"), ] ...  in crib_data
    crib_data[data["term"]][data["subject"]]["photos"][data["number"]] = new_photos

    for photo in data["photos"]:
        shutil.move(photo, dest_photo_path)

    # delete old dir (aka 2376827356) in temp
    Path(data["photos"][0]).parent.rmdir()
    await state.finish()
