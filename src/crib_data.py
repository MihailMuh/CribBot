import os
import re
from pathlib import Path
from typing import List

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
                tickets_dict[int(current_ticket)] = {
                    "is_additional": False,
                    "photos": [path_to_dir / t for t in tickets[i:j]],
                }
                i = j - 1

                break
        else:
            tickets_dict[int(current_ticket)] = {
                "is_additional": False,
                "photos": [path_to_dir / t for t in tickets[i:]],
            }
            break

        i += 1

    return tickets_dict


'''
structure of crib_data:
{
    "term_1": {
        "matanalysis": {
            "tickets": {
                45: {
                    "is_additional": False,
                    "photos": [Path("45_1.jpg"), Path("45_2.jpg")],
                },
                46: {
                    "is_additional": True,
                    "photos": [Path("46_1.jpg"), Path("46_2.jpg")],
                },
            },
            "ticket_numbers": "12 - сложение функций\n....."
        }
    },
}
'''

translate: dict = dict()
crib_data: dict = dict()


def generate_crib_data():
    global translate, crib_data

    with open(BASE_DIR / "photo" / "translate.json", "rb") as binary_file:
        translate = loads(binary_file.read())
    walking: list = list(os.walk(BASE_DIR / "photo"))

    # get terms from /photo dir
    for _dir in walking.pop(0)[1]:
        crib_data[_dir] = dict()

    _init_subject_dirs_in_crib_data(walking)

    # filter elements where photo exists
    for path, dirs, photos in filter(lambda _tuple: _tuple[0].split("/")[-1] in translate.keys(), walking):
        split: list = path.split("/")  # ["home", "user", "Desktop", "CribBot", "photo", "term_1", "matanalysis"]
        term: str = split[-2]
        subject: str = split[-1]

        with open(BASE_DIR / "ticket_numbers" / term / f"{subject}.txt", encoding="utf-8") as file:
            photos_dict: dict = extract_photos_to_dict(Path(path), photos)
            input_data: list = file.readlines()

            # if finds 1. 2. 34. etc, remove point
            all_tickets_numbers: List[int] = []
            tickets_solid_string: str = ""

            for i, line in enumerate(input_data):
                try:
                    ticket_number: int = _get_ticket_number_from_line(line)
                    all_tickets_numbers.append(ticket_number)

                    if "ABOBA" in line:
                        line = "".join(line.split("ABOBA", 1))
                        if photos_dict.get(ticket_number):
                            photos_dict[ticket_number]["is_additional"] = True

                    if ticket_number in photos_dict.keys():
                        line = f"🫡 {line}"
                except IndexError:
                    # don't find ticket number at the beginning of the line
                    # and at the beginning of the NEXT line,
                    # so line must be without \n
                    try:
                        _get_ticket_number_from_line(input_data[i + 1])
                    except IndexError:
                        line = line.replace("\n", " ")

                if line[-1] != "\n":
                    line += "\n"
                tickets_solid_string += line

            if min(all_tickets_numbers) not in photos_dict.keys():
                photos_dict[min(all_tickets_numbers)] = []
            if max(all_tickets_numbers) not in photos_dict.keys():
                photos_dict[max(all_tickets_numbers)] = []

            crib_data[term][subject] = {
                "tickets": photos_dict,
                "ticket_numbers": tickets_solid_string,
            }


def _get_ticket_number_from_line(line: str):
    return int(re.findall(r'\d+', line)[0])


def _init_subject_dirs_in_crib_data(walking: list):
    for path, dirs, photos in filter(lambda _tuple: _tuple[1], walking):
        split: list = path.split("/")  # ["home", "user", "Desktop", "CribBot", "photo", "term_1", "matanalysis"]
        crib_data[split[-1]] = {_dir: dict() for _dir in dirs}


generate_crib_data()
