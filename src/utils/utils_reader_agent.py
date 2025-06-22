from flock.core import FlockAgent

from agents.ticket_agent import TicketAgent


def setup_reader_agent() -> FlockAgent:
    reader_agent = TicketAgent(
        name="ticket_reader_agent",
    )
    return reader_agent.create_issue_reader_agent()
