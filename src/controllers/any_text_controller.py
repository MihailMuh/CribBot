from aiogram import types

from ..core import dispatcher


@dispatcher.message_handler()
async def any_text_handler(message: types.Message):
    await message.answer("Что-то я тебя не понял). Ты выбрал семестр и предмет экзамена?")
