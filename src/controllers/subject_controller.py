from aiogram import types

from src.buttons import subject_buttons
from src.cache.user_cache import cache
from src.core.core import dispatcher
from src.crib_data import translate
from src.string_utils import get_subject_with_first_char_lower_case


@dispatcher.message_handler(commands=['subject'])
async def choose_subject(message: types.Message):
    if not (term := cache.get_term(message.from_user.id)):
        return await message.answer("Нужно знать семестр, чтобы выбрать предмет!")

    await message.answer("Выбери, по какому предмету экзамен", reply_markup=subject_buttons[term])


@dispatcher.callback_query_handler(text=translate.keys())
async def set_subject_from_button(call: types.CallbackQuery):
    await cache.set_subject(call.from_user.id, call.data)
    await call.message.answer(f"Решения будут выдаваться для предмета: "
                              f"{get_subject_with_first_char_lower_case(call.data)}")
