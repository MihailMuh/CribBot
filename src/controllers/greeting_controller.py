from aiogram import types

from src.core.core import dispatcher

greeting: str = """
Привет!
Это бот, который отправляет решения на билеты (если они есть :)) по конкретному экзамену

Список доступных команд:
/start - запустить это приветственное сообщение
/term - задать семестр экзамена
/subject - задать предмет для экзамена
/tickets - получить список вопросов
/upload - загрузить решения на вопрос экзамена
/support - поддержать автора :)

Для получения решения нужно писать только НОМЕР вопроса
"""


@dispatcher.message_handler(commands=['start'])
async def greeting_message(message: types.Message):
    await message.answer(greeting)
