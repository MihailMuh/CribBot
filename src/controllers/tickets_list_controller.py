from aiogram import types

from ..core import dispatcher
from ..crib_data import crib_data
from ..user import get_term, get_subject


@dispatcher.message_handler(commands=['tickets'])
async def get_tickets_list(message: types.Message):
    if not get_term():
        return await message.answer("Семестр не выбран!")
    if not get_subject():
        return await message.answer("Предмет не выбран!")

    await message.answer(crib_data[get_term()][get_subject()]["ticket_numbers"])
