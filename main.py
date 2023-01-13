import redis.asyncio as redis
from aiogram import executor, types, Dispatcher

from src.constants import REDIS_SOCKET, REDIS_DB
from src.core import dispatcher
from src.user import set_term, set_subject, get_term, get_subject, cache

redis_db: redis.Redis


async def redis_startup():
    global redis_db
    redis_db = redis.Redis(unix_socket_path=REDIS_SOCKET, db=REDIS_DB, decode_responses=True)

    set_term(await redis_db.get("term"))
    set_subject(await redis_db.get("subject"))

    print(get_term(), get_subject())


async def startup(dp: Dispatcher):
    await redis_startup()
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить приветственный диалог"),
        types.BotCommand("subject", "Установить предмет для экзамена"),
        types.BotCommand("term", "Установить семестр экзамена"),
        types.BotCommand("tickets", "Получить список вопросов"),
    ])


async def shutdown(dp: Dispatcher):
    await redis_db.mset(cache)

    await redis_db.save()
    await redis_db.close()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
