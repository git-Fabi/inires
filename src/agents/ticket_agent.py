from flock.core import FlockFactory, FlockAgent

from models.ticket import Ticket
from models.ticket_context import TicketContext


class TicketAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = (
            "You are a very good reader, you love reading and understanding the "
            "most important context. Most of the time you read "
            "github tickets. It is your task to read and understand these tickets, "
            "then you should explain the context such that a developer can "
            "implement a solution for the ticket according to your context."
            "Understand that your output will be used by a developer to implement a solution, "
            "so you should be as precise and detailed as possible."
        )

    def create_issue_reader_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input=Ticket.get_representation_for_agent(),
            output=TicketContext.get_representation_for_agent(),
            temperature=1.0,
            max_tokens=16384,
        )
