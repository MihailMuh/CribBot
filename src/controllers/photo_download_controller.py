from aiogram import types
from aiogram.types import InputMediaPhoto, InputFile

from .quick_checks import get_term_subject
from ..core import dispatcher
from ..core import telegram_bot
from ..crib_data import crib_data
from ..models.ticket import Ticket
from ..string_utils import get_pretty_photo_name


def get_photos(ticket: Ticket) -> list:
    photos: list = crib_data[ticket.term][ticket.subject]["photos"].get(ticket.number)

    return [InputFile(photo) for photo in photos] if photos else []


def get_media(ticket: Ticket) -> list:
    photos: list = get_photos(ticket)

    if not photos:
        return []

    media_group: list = [InputMediaPhoto(media=photos[0], caption=get_pretty_photo_name(ticket))]
    for i in range(1, len(photos)):
        media_group.append(InputMediaPhoto(media=photos[i]))

    return media_group


@dispatcher.message_handler(regexp=r'^([\s\d]+)$')  # only numbers
async def send_photo_to_user(message: types.Message):
    ticket: Ticket = Ticket(int(message.text), *(await get_term_subject(message)))
    if not ticket.term:  # if no term or subject selected, get_term_subject already answered for user
        return

    if not ticket.is_number_valid():
        return await message.answer("Нет такого номера вопроса!")

    media: list = get_media(ticket)
    if not media:
        return await message.answer("Решения на этот вопрос еще не появилось(")

    await telegram_bot.send_media_group(chat_id=message.from_user.id, media=media)
