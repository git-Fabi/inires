from flock.core import FlockAgent

from agents.ticket_agent import TicketAgent


def setup_ticket_agent() -> FlockAgent:
    ticket_agent = TicketAgent(
        name="ticket_reader_agent",
    )
    return ticket_agent.create_ticket_agent()
