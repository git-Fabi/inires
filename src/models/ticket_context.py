class TicketContext:
    def __init__(self) -> None:
        self.ticket_context: str = ""

    @staticmethod
    def get_representation_for_agent() -> str:
        return (
            "ticket_context: str | The core context of the ticket describing "
            "the problem and what it tries to solve. "
            "This should be a concise summary of the ticket's content. "
            "The format which must be returned is JSON"
        )
