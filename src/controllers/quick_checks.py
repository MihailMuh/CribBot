from aiogram import types

from ..user_cache import cache


async def get_term_subject(message: types.Message) -> tuple:
    user_id: int = message.from_user.id

    term: str = cache.get_term(user_id)
    subject: str = cache.get_subject(user_id)

    if not term:
        await message.answer("Семестр не выбран!")
        return tuple()
    if not subject:
        await message.answer("Предмет не выбран!")
        return tuple()

    return term, subject
