class Ticket:
    def __init__(self, ticket_title: str, ticket_body: str, ticket_number: str) -> None:
        self.title: str = ticket_title
        self.body: str = ticket_body
        self.number: str = ticket_number

    def to_dict(self) -> dict:
        return {
            "ticket_title": self.title,
            "ticket_body": self.body,
            "ticket_number": self.number,
        }

    @staticmethod
    def get_representation_for_agent() -> str:
        return (
            "ticket_title: str | The title of the ticket, "
            "ticket_body: str | The description of the ticket, "
            "ticket_number: str | Unique identifier for the ticket"
        )
