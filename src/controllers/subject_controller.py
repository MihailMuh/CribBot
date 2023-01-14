from aiogram import types

from ..buttons import subject_buttons
from ..core import dispatcher
from ..crib_data import translate
from ..string_utils import get_subject_with_first_char_lower_case
from ..user_cache import cache


@dispatcher.message_handler(commands=['subject'])
async def choose_subject(message: types.Message):
    term: str = cache.get_term(message.from_user.id)
    if not term:
        return await message.answer("Нужно знать семестр, чтобы выбрать предмет!")

    await message.answer("Выбери, по какому предмету экзамен", reply_markup=subject_buttons[term])


@dispatcher.callback_query_handler(text=translate.keys())
async def set_subject_from_button(call: types.CallbackQuery):
    await cache.set_subject(call.from_user.id, call.data)
    await call.message.answer(
        f"Решения будут выдаваться для предмета: {get_subject_with_first_char_lower_case(call.data)}")
