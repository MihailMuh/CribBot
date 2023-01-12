from aiogram import types
from aiogram.types import InputFile, InputMediaPhoto

from .constants import BASE_DIR
from .core import dispatcher, telegram_bot


def get_photos_by_number(number: int) -> list:
    photos: list = []
    try:
        i: int = 0
        while True:
            i += 1
            photos.append(InputFile(BASE_DIR / "photo" / "matanalysis" / "term_1" / f"{number}_{i}.jpg"))
    except FileNotFoundError:
        return photos


def get_media_by_number(number: int) -> list:
    photos: list = get_photos_by_number(number)

    if not photos:
        return []

    media_group: list = [InputMediaPhoto(media=photos[0], caption=str(number))]
    for i in range(1, len(photos)):
        media_group.append(InputMediaPhoto(media=photos[i]))

    return media_group


@dispatcher.message_handler()
async def send_photo_to_user(message: types.Message) -> None | types.Message:
    try:
        ticket_number = int(message.text)
    except ValueError:
        return await message.answer("Номер билета должен быть числом!")

    if not (18 <= ticket_number <= 62):
        return await message.answer("Нет такого номера билета!")

    media: list = get_media_by_number(ticket_number)
    if not media:
        return await message.answer("Нет такого билета!")

    await telegram_bot.send_media_group(chat_id=message.from_user.id, media=media)
