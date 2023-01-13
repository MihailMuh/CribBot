cache: dict = {
    "term": "",
    "subject": "",
}


def set_term(term: str) -> None:
    cache["term"] = term


def get_term() -> str:
    return cache["term"]


def get_subject() -> str:
    return cache["subject"]


def set_subject(subject: str) -> None:
    cache["subject"] = subject
