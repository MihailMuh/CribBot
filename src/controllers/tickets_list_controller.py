from aiogram import types

from .quick_checks import get_term_subject
from ..core import dispatcher
from ..crib_data import crib_data


@dispatcher.message_handler(commands=['tickets'])
async def get_tickets_list(message: types.Message):
    term, subject = get_term_subject(message)
    if not term:  # if no term or subject selected, get_term_subject already answered for user
        return

    await message.answer(crib_data[term][subject]["ticket_numbers"])
