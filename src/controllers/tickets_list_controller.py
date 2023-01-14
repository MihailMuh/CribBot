from aiogram import types

from src.controllers.validator import is_term_subject_valid
from src.core.core import dispatcher
from src.crib_data import crib_data


async def send_long_message(message: types.Message, data: str):
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            await message.answer(data[x:x + 4096])
        return

    await message.answer(data)


@dispatcher.message_handler(commands=['tickets'])
async def get_tickets_list(message: types.Message):
    term, subject = await is_term_subject_valid(message)
    if (not term) and (not subject):  # if no term or subject selected, get_term_subject already answered for user
        return

    await send_long_message(message, crib_data[term][subject]["ticket_numbers"])
