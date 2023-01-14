from functools import lru_cache

from src.controllers.photo_controllers.photo_download_controller import Ticket
from src.crib_data import translate
from src.cache.user_cache import cache


def get_pretty_photo_name(ticket: Ticket) -> str:
    return f"{ticket.number} - {get_subject_with_first_char_lower_case(ticket.subject)}, {get_term_translate(ticket.term)}"


@lru_cache(1024)
def get_subject_with_first_char_lower_case(subject: str) -> str:
    subject: str = translate[subject]
    return f"{subject[0].lower()}{subject[1:]}"


@lru_cache(1024)
def get_term_translate(term: str) -> str:
    return f"{term.split('_')[1]} семестр"


@lru_cache(1024)
def get_term_number(user_id: int) -> str:
    return cache.get_term(user_id).split('_')[1]
