from aiogram import types

from src.cache.user_cache import cache


# returns (term, subject) if data valid otherwise returns ()
async def is_term_subject_valid(message: types.Message) -> tuple:
    user_id: int = message.from_user.id

    term: str = cache.get_term(user_id)
    subject: str = cache.get_subject(user_id)

    if not term:
        await message.answer("Семестр не выбран!")
    if not subject:
        await message.answer("Предмет не выбран!")

    return term, subject
