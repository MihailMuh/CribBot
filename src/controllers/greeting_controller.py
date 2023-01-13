from aiogram import types

from ..core import dispatcher

greeting: str = """
Привет!
Это бот, который отправляет решения на билеты (если они есть :)) по конкретному экзамену

Список доступных команд:
/start - запустить это приветственное сообщение
/term - установить семестр экзамена
/subject - установить предмет для экзамена
/tickets - получить список вопросов

Для получения решения нужно писать только НОМЕР вопроса
"""


@dispatcher.message_handler(commands=['start'])
async def greeting_message(message: types.Message):
    await message.answer(greeting)
