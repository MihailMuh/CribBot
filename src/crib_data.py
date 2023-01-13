import os
from pathlib import Path

from orjson import loads

from .constants import BASE_DIR
from .user import get_term, get_subject


def get_min_number_of_tickets() -> int:
    return min(crib_data[get_term()][get_subject()]["photos"].keys())


def get_max_number_of_tickets() -> int:
    return max(crib_data[get_term()][get_subject()]["photos"].keys())


def extract_photos_to_dict(path_to_dir: Path, tickets: list) -> dict:
    tickets.sort()
    tickets_dict: dict = dict()
    i: int = 0

    while i < len(tickets):
        current_ticket: str = tickets[i]

        for j in range(i + 1, len(tickets)):
            next_ticket: str = tickets[j]

            if current_ticket[:current_ticket.index("_")] != next_ticket[:next_ticket.index("_")]:
                tickets_dict[int(current_ticket[:current_ticket.index("_")])] = [path_to_dir / t for t in tickets[i:j]]
                i = j - 1
                break

        i += 1

    return tickets_dict


# structure of crib_data:
# {
#     "term_1": {
#         "matanalysis": {
#             "photos": {
#                 45: [Path("45_1.jpg"), Path("45_2.jpg")],
#                 46: [Path("46_1.jpg")]
#             },
#             "ticket_numbers": "12 - сложение функций\n....."
#         }
#     },
# }

with open(BASE_DIR / "photo" / "translate.json", "rb") as binary_file:
    translate: dict = loads(binary_file.read())
crib_data: dict = dict()

# filter elements where photo exists
for path, dirs, photos in filter(lambda _tuple: _tuple[2], list(os.walk(BASE_DIR / "photo"))[1:]):
    split: list = path.split("/")  # ["home", "user", "Desktop", "CribBot", "photo", "term_1", "matanalysis"]
    term: str = split[-2]
    subject: str = split[-1]

    with open(BASE_DIR / "ticket_numbers" / term / f"{subject}.txt", encoding="utf-8") as file:
        crib_data[term] = {
            subject: {
                "photos": extract_photos_to_dict(Path(path), photos),
                "ticket_numbers": "".join(file.readlines()),
            }
        }