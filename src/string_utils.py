from functools import lru_cache

from .crib_data import translate
from .user import get_subject, get_term


@lru_cache(1024)
def get_pretty_photo_name(ticket_number: int) -> str:
    return f"{ticket_number} - {get_subject_with_first_char_lower_case()}, {get_term_translate(get_term())}"


def get_subject_with_first_char_lower_case() -> str:
    subject: str = translate[get_subject()]
    return f"{subject[0].lower()}{subject[1:]}"


@lru_cache(32)
def get_term_translate(term: str) -> str:
    return f"{term.split('_')[1]} семестр"


def get_term_number() -> str:
    return get_term().split('_')[1]
