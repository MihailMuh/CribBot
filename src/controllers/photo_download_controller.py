from aiogram import types
from aiogram.types import InputMediaPhoto, InputFile

from ..core import dispatcher
from ..core import telegram_bot
from ..crib_data import get_min_number_of_tickets, get_max_number_of_tickets, crib_data
from ..string_utils import get_pretty_photo_name
from ..user import get_term, get_subject


def get_photos_by_number(number: int) -> list:
    return [InputFile(photo) for photo in crib_data[get_term()][get_subject()]["photos"][number]]


def get_media_by_number(number: int) -> list:
    photos: list = get_photos_by_number(number)

    if not photos:
        return []

    media_group: list = [InputMediaPhoto(media=photos[0], caption=get_pretty_photo_name(number))]
    for i in range(1, len(photos)):
        media_group.append(InputMediaPhoto(media=photos[i]))

    return media_group


@dispatcher.message_handler(regexp=r'^([\s\d]+)$')
async def send_photo_to_user(message: types.Message):
    if not get_term():
        return await message.answer("Семестр не выбран!")
    if not get_subject():
        return await message.answer("Предмет не выбран!")

    ticket_number = int(message.text)

    if not (get_min_number_of_tickets() <= ticket_number <= get_max_number_of_tickets()):
        return await message.answer("Нет такого номера вопроса!")

    media: list = get_media_by_number(ticket_number)
    if not media:
        return await message.answer("Решения на этот вопрос еще не появилось(")

    await telegram_bot.send_media_group(chat_id=message.from_user.id, media=media)
