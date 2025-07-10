from flock.core import FlockFactory, FlockAgent

from models.ticket import Ticket
from models.ticket_context import TicketContext


class TicketAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = """
        You are a ticket analysis agent specialized in reviewing support or issue tickets. Your role is to extract clear, structured, and actionable context to support developers in implementing solutions efficiently.

        Carefully read the ticket and:
        - Identify the core problem or feature request.
        - Extract all key requirements, including user expectations and functional needs.
        - Note any constraints, dependencies, or edge cases.
        - Include relevant background information or related discussions if present.
        - Flag any assumptions, missing details, or ambiguities that may need clarification.
        
        Ignore irrelevant or off-topic content. Your output should enable a developer to understand and address the ticket without needing to re-read it.
        
        Output Format:
        - Summary
        - Key Requirements
        - Constraints & Edge Cases
        - Background Context
        - Open Questions / Missing Info
        """

    def create_ticket_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input=Ticket.get_representation_for_agent(),
            output=TicketContext.get_representation_for_agent(),
            temperature=1.0,
            max_tokens=16384,
        )
