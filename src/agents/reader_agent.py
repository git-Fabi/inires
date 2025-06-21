from flock.core import FlockFactory, FlockAgent

from models.Ticket import Ticket
from models.TicketContext import TicketContext


class IssueReaderAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.agent = None
        self.description = (
            "You are a reader agent that reads and processes "
            "tickets. Your task is to read the ticket and "
            "generate a context such that a developer can "
            "implement a solution for the ticket according to "
            "best practices."
        )

    def create_issue_reader_agent(self) -> FlockAgent:
        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input=Ticket.get_representation_for_agent(),
            output=TicketContext.get_representation_for_agent(),
            temperature=1.0,
            max_tokens=16384,
        )
        return self.agent
