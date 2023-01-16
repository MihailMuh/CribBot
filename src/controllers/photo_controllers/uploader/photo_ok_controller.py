import shutil
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.constants import BASE_DIR
from src.controllers.photo_controllers.uploader.upload_state import UploadStates
from src.core.core import dispatcher
from src.crib_data import crib_data, generate_crib_data


@dispatcher.callback_query_handler(state=UploadStates.rate_photos, text="ok")
async def photo_ok(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Решения успешно сохранены")

    data: dict = await state.get_data()
    dest_photo_path: Path = BASE_DIR / "photo" / data["term"] / data["subject"]

    if data.get("new_ticket_name"):
        # write new ticket to .txt
        with open(BASE_DIR / "ticket_numbers" / data["term"] / f"{data['subject']}.txt", "a") as file:
            file.write(f"{data['number']}. ABOBA{data['new_ticket_name']}\n")

    # delete old photos
    if old_photos := crib_data[data["term"]][data["subject"]]["tickets"].get(data["number"]):
        for photo in old_photos["photos"]:
            photo.unlink()

    for photo in data["photos"]:
        shutil.move(photo, dest_photo_path)

    # delete old dir (aka 2376827356) in temp
    Path(data["photos"][0]).parent.rmdir()

    generate_crib_data()
    await state.finish()
