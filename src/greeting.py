from aiogram import types

from .core import dispatcher

with open("ticket_numbers/matananalysis/term_1.txt", encoding="utf-8") as file:
    tickets_numbers: str = "".join(file.readlines())


@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.reply(f"""
        Привет!\n
        Список доступных билетов:\n
        \n
        {tickets_numbers}\n
        Напиши НОМЕР одного из них, чтобы получить фото решения
    """)
