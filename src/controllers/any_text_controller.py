from aiogram import types

from src.core.core import dispatcher


@dispatcher.message_handler()
async def any_text_handler(message: types.Message):
    if message.text.lower() in ["абоба", "aboba"]:
        return await message.answer("❤️")
    await message.answer("🤦")
