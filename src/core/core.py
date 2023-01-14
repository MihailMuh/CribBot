import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from src.constants import API_TOKEN, REDIS_SOCKET, REDIS_DB, REDIS_DB_FSM
from src.core.photo_middleware import PhotoMiddleware

redis_db: redis.Redis = redis.Redis(unix_socket_path=REDIS_SOCKET, db=REDIS_DB, decode_responses=True)

telegram_bot: Bot = Bot(token=API_TOKEN)
dispatcher: Dispatcher = Dispatcher(telegram_bot, storage=RedisStorage2(unix_socket_path=REDIS_SOCKET, db=REDIS_DB_FSM))
dispatcher.middleware.setup(PhotoMiddleware())
