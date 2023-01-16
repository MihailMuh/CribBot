import dataclasses

from src.crib_data import crib_data


@dataclasses.dataclass
class Ticket:
    def __init__(self, number: int, term: str = "", subject: str = ""):
        self.number: int = number
        self.term: str = term
        self.subject: str = subject

    def is_number_valid(self) -> bool:
        all_tickets: dict = crib_data[self.term][self.subject]["tickets"].keys()

        if all_tickets:
            # self.number may have any value, because user can add new ticket,
            # so we check two conditions
            return (min(all_tickets) <= self.number <= max(all_tickets)) or (self.number in all_tickets)
