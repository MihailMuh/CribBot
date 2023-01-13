from aiogram import Bot, Dispatcher

from .constants import API_TOKEN

telegram_bot: Bot = Bot(token=API_TOKEN)
dispatcher: Dispatcher = Dispatcher(telegram_bot)
