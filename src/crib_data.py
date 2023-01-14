import os
import re
from pathlib import Path

from orjson import loads

from src.constants import BASE_DIR


def extract_photos_to_dict(path_to_dir: Path, tickets: list) -> dict:
    tickets.sort()

    tickets_dict: dict = dict()
    i: int = 0

    while i < len(tickets):
        current_ticket: str = tickets[i][:tickets[i].index("_")]

        for j in range(i + 1, len(tickets)):
            next_ticket: str = tickets[j]

            if current_ticket != next_ticket[:next_ticket.index("_")]:
                tickets_dict[int(current_ticket)] = [path_to_dir / t for t in tickets[i:j]]
                i = j - 1

                break
        else:
            tickets_dict[int(current_ticket)] = [path_to_dir / t for t in tickets[i:]]
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
walking: list = list(os.walk(BASE_DIR / "photo"))
crib_data: dict = {_dir: dict() for _dir in walking.pop(0)[1]}

# init dirs
for path, dirs, photos in filter(lambda _tuple: _tuple[1], walking):
    split: list = path.split("/")  # ["home", "user", "Desktop", "CribBot", "photo", "term_1", "matanalysis"]
    crib_data[split[-1]] = {_dir: dict() for _dir in dirs}

# filter elements where photo exists
for path, dirs, photos in filter(lambda _tuple: _tuple[0].split("/")[-1] in translate.keys(), walking):
    split: list = path.split("/")  # ["home", "user", "Desktop", "CribBot", "photo", "term_1", "matanalysis"]
    term: str = split[-2]
    subject: str = split[-1]

    with open(BASE_DIR / "ticket_numbers" / term / f"{subject}.txt", encoding="utf-8") as file:
        photos_dict: dict = extract_photos_to_dict(Path(path), photos)
        ticket_numbers: str = "".join(file.readlines())

        # it finds 1. 2. 34. etc, so we remove point
        all_tickets: list = list(map(lambda x: int(x.replace(".", "")), re.findall(r'\d+\.', ticket_numbers)))

        if min(all_tickets) not in photos_dict.keys():
            photos_dict[min(all_tickets)] = []
        if max(all_tickets) not in photos_dict.keys():
            photos_dict[max(all_tickets)] = []

        crib_data[term][subject] = {
            "photos": photos_dict,
            "ticket_numbers": ticket_numbers,
        }
