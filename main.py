from aiogram import executor, types, Dispatcher

from src.core.core import dispatcher, redis_db


async def init_redis():
    redis_cache: dict = {int(key): await redis_db.hgetall(key) for key in await redis_db.keys()}

    if redis_cache:
        from src.cache.user_cache import cache

        cache.set_primary_cache(redis_cache)
        print("Cache is being restored!")
    else:
        print("Cache isn't being restored!")


async def startup(dp: Dispatcher):
    await init_redis()
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить приветственный диалог"),
        types.BotCommand("subject", "Задать предмет для экзамена"),
        types.BotCommand("term", "Задать семестр экзамена"),
        types.BotCommand("tickets", "Получить список вопросов"),
        types.BotCommand("upload", "Загрузить решения на вопрос"),
        types.BotCommand("support", "Поддержать автора :)"),
    ])


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False, on_startup=startup)
