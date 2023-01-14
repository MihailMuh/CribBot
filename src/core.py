import redis.asyncio as redis
from aiogram import Bot, Dispatcher

from .constants import API_TOKEN, REDIS_SOCKET, REDIS_DB

telegram_bot: Bot = Bot(token=API_TOKEN)
dispatcher: Dispatcher = Dispatcher(telegram_bot)
redis_db: redis.Redis = redis.Redis(unix_socket_path=REDIS_SOCKET, db=REDIS_DB, decode_responses=True)
