from aiogram import types
from aiogram.dispatcher.filters import Text

from ..buttons import term_buttons
from ..core import dispatcher
from ..string_utils import get_term_number
from ..user_cache import cache


@dispatcher.message_handler(commands=['term'])
async def choose_term(message: types.Message):
    await message.answer("Выбери, по какому семестру выдавать решения", reply_markup=term_buttons)


@dispatcher.callback_query_handler(Text(contains="term"))
async def set_term_from_button(call: types.CallbackQuery):
    user_id: int = call.from_user.id

    await cache.set_term(user_id, call.data)
    await call.message.answer(f"Решения будут выдаваться для семестра № {get_term_number(user_id)}")
