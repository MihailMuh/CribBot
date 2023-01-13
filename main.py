from aiogram import executor, types, Dispatcher

from src.core import dispatcher


async def startup(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить приветственный диалог"),
        types.BotCommand("subject", "Установить предмет для экзамена"),
        types.BotCommand("term", "Установить семестр экзамена"),
        types.BotCommand("tickets", "Получить список вопросов"),
    ])


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=startup)
