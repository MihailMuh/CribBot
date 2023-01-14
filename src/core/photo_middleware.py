from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class PhotoMiddleware(BaseMiddleware):
    messages: dict = {}

    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.messages[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.messages[message.media_group_id] = [message]

            message.conf["is_last"] = True
            data["messages"] = self.messages[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if message.conf.get("is_last") and message.media_group_id:
            del self.messages[message.media_group_id]
