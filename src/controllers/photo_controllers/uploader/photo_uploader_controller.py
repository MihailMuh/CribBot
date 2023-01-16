from pathlib import Path
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, InlineKeyboardMarkup, ParseMode, InputMediaPhoto, InputFile

from src.buttons import button_cancel, button_ok, button_bad
from src.cache.user_cache import cache
from src.constants import SECRET_KEYS, BASE_DIR
from src.controllers.photo_controllers.uploader.upload_state import UploadStates
from src.controllers.validator import is_term_subject_valid
from src.core.core import dispatcher
from src.models.ticket import Ticket
from src.string_utils import get_subject_with_first_char_lower_case, get_term_translate, get_pretty_photo_name


@dispatcher.message_handler(commands=['upload'])
async def ask_secret_key(message: types.Message):
    term, subject = await is_term_subject_valid(message)
    if (not term) and (not subject):  # if no term or subject selected, get_term_subject already answered for user
        return

    await message.answer(f"Ты хочешь добавить решения по предмету: "
                         f"{get_subject_with_first_char_lower_case(subject)}, "
                         f"{get_term_translate(term)}.\n"
                         f"Для этого введи секретный ключ",
                         reply_markup=InlineKeyboardMarkup(row_width=1).add(button_cancel))
    await UploadStates.check_key.set()


@dispatcher.message_handler(state=UploadStates.check_key)
async def check_key(message: types.Message):
    if message.text not in SECRET_KEYS:
        return await message.answer("Неверный ключ! Пробуй еще раз")

    await message.answer("Ключ верный! Теперь введи НОМЕР билета, на который высылаешь решение",
                         reply_markup=InlineKeyboardMarkup(row_width=1).add(button_cancel))
    await UploadStates.next()


async def ask_send_photo(message: types.Message):
    await message.answer("Теперь отправляй сюда фотографии (не более 10! остальные - скипнутся).\n"
                         "Можно все одним сообщением, можно - по отдельности\n"
                         "Они будут сохранятся в том порядке, в каком ты отправишь\n"
                         "Когда закончишь, напиши `КОНЕЦ`",
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=InlineKeyboardMarkup(row_width=1).add(button_cancel))

    await UploadStates.upload_photo.set()


@dispatcher.message_handler(state=UploadStates.ticket_number)
async def ticket_number(message: types.Message, state: FSMContext):
    try:
        user_id: int = message.from_user.id
        term: str = cache.get_term(user_id)
        subject: str = cache.get_subject(user_id)
        ticket: Ticket = Ticket(int(message.text), term, subject)

        if int(message.text) <= 0:
            raise ValueError
    except ValueError:
        await message.answer("🤦")
        return await message.answer("Это не номер... Пробуй еще раз")

    await state.update_data(ticket.__dict__, photos=[], id=str(message.from_user.id))

    if not ticket.is_number_valid():
        await UploadStates.add_ticket_name.set()
        return await message.answer("Такого номера вопроса нет, значит, будет добавляться новый пункт\n"
                                    "Напиши название нового вопроса и после этого введи `КОНЕЦ`\n"
                                    "Если ты отправишь несколько сообщений, возьмется только последнее!",
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=InlineKeyboardMarkup(row_width=1).add(button_cancel))

    await ask_send_photo(message)


@dispatcher.message_handler(state=UploadStates.add_ticket_name)
async def add_ticket_name(message: types.Message, state: FSMContext):
    if message.text == "КОНЕЦ":
        return await ask_send_photo(message)

    await state.update_data(new_ticket_name=message.text.replace("\n", ". "))


def get_photo(data: dict, photo_suffix: int) -> Path:
    return BASE_DIR / "temp" / data["term"] / data["subject"] / data["id"] / f"{data['number']}_{photo_suffix}.jpg"


@dispatcher.message_handler(content_types=ContentType.PHOTO, state=UploadStates.upload_photo)
async def upload_photo(msg: types.Message, state: FSMContext, messages: List[types.Message] | None = None):
    data: dict = await state.get_data()
    photos: list = data["photos"]

    if not messages:
        messages = [msg]

    for message in messages:
        path: Path = get_photo(data, len(photos) + 1)
        photos.append(str(path))
        await message.photo[-1].download(destination_file=path)

    await state.update_data(photos=photos)


@dispatcher.message_handler(state=UploadStates.upload_photo)
async def finish(message: types.Message, state: FSMContext):
    if message.text != "КОНЕЦ":
        return await rate_waiting(message)

    data: dict = await state.get_data()
    photos: list = list(map(Path, data["photos"]))

    if not photos:
        await message.answer("🤦")
        return await message.answer("Ты не отправил ни одного фото...")

    ticket: Ticket = Ticket(data['number'], data["term"], data["subject"])
    media: list = [InputMediaPhoto(media=InputFile(photos.pop(0)), caption=get_pretty_photo_name(ticket))] + \
                  [InputMediaPhoto(media=InputFile(photo)) for photo in photos]

    if len(media) > 10:
        media = media[:10]

    await message.answer_media_group(media=media)
    await message.answer("Твои фото будут выглядеть так",
                         reply_markup=InlineKeyboardMarkup(row_width=1)
                         .add(button_ok).add(button_bad).add(button_cancel))
    await UploadStates.next()


@dispatcher.message_handler(state=UploadStates.rate_photos)
async def rate_waiting(message: types.Message):
    await message.answer("🤦")
    await message.answer("Возникли проблемы? Жми на любую из кнопок ОТМЕНА выше, и начни все заново!")
