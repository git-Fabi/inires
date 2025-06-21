class TicketContext:
    def __init__(self) -> None:
        self.ticket_id: str = ""
        self.best_practices: str = ""
        self.ticket_context: str = ""

    @staticmethod
    def get_representation_for_agent() -> str:
        return (
            "ticket_id: str | Unique identifier for the ticket, "
            "best_practices: str | Best practices related to the ticket if applicable, "
            "ticket_context: str | The core context of the ticket describing the problem and what it tries to solve"
        )
