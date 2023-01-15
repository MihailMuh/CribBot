from aiogram import types
from aiogram.types import ParseMode

from src.core.core import dispatcher


@dispatcher.message_handler(commands=['support'])
async def support(message: types.Message):
    await message.answer("Если ты хочешь не только морально поддержать разработчика: @mihalisM,\n"
                         "то можешь скинуть по номеру `+79087016312` какую-то сумму 🙃",
                         parse_mode=ParseMode.MARKDOWN)
