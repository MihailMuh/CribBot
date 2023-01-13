from aiogram import types

from ..buttons import subject_buttons
from ..core import dispatcher
from ..crib_data import translate
from ..string_utils import get_subject_with_first_char_lower_case
from ..user import get_term, set_subject


@dispatcher.message_handler(commands=['subject'])
async def choose_subject(message: types.Message):
    if not get_term():
        return await message.answer("Нужно знать семестр, чтобы выбрать предмет!")

    await message.answer("Выбери, по какому предмету экзамен", reply_markup=subject_buttons[get_term()])


@dispatcher.callback_query_handler(text=translate.keys())
async def set_subject_from_button(call: types.CallbackQuery):
    set_subject(call.data)
    await call.message.answer(f"Решения будут выдаваться для предмета: {get_subject_with_first_char_lower_case()}")
