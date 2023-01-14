from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .crib_data import crib_data, translate
from .string_utils import get_term_translate


def get_subjects_from_term(_subjects: dict) -> InlineKeyboardMarkup:
    subj_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for subject in _subjects.keys():
        subj_buttons.add(InlineKeyboardButton(text=translate[subject], callback_data=subject))
    return subj_buttons


term_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
subject_buttons: dict = {}

for term, subjects in crib_data.items():
    term_buttons.add(InlineKeyboardButton(text=get_term_translate(term), callback_data=term))
    subject_buttons[term] = get_subjects_from_term(subjects)
