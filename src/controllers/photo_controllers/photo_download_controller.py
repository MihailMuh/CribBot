from aiogram import types
from aiogram.types import InputMediaPhoto, InputFile

from src.controllers.validator import is_term_subject_valid
from src.core.core import dispatcher
from src.crib_data import crib_data
from src.models.ticket import Ticket
from src.string_utils import get_pretty_photo_name


def get_photos(ticket: Ticket) -> list:
    ticket_number: dict = crib_data[ticket.term][ticket.subject]["tickets"].get(ticket.number)

    return [InputFile(photo) for photo in ticket_number["photos"]] if ticket_number else []


def get_media(ticket: Ticket) -> list:
    photos: list = get_photos(ticket)

    if not photos:
        return []

    media: list = [InputMediaPhoto(media=photos[0], caption=get_pretty_photo_name(ticket))]
    for i in range(1, len(photos)):
        media.append(InputMediaPhoto(media=photos[i]))

    return media


@dispatcher.message_handler(regexp=r'^([\s\d]+)$')  # only numbers
async def send_photo_to_user(message: types.Message):
    ticket: Ticket = Ticket(int(message.text), *(await is_term_subject_valid(message)))
    if not ticket.term:  # if no term or subject selected, get_term_subject already answered for user
        return

    if not ticket.is_number_valid():
        return await message.answer("Нет такого номера вопроса!")

    media: list = get_media(ticket)
    if not media:
        return await message.answer("Решения на этот вопрос еще не появилось(")

    await message.answer_media_group(media=media)
