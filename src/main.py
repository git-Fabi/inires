from models.ticket import Ticket
from utils.utils_agents import runner, setup_agents
from src.utils.utils_agents import setup_agents, runner

def main(ticket: Ticket, repository: str) -> str:
    inires_flock = setup_agents()
    result = runner(inires_flock, ticket=ticket, repository)

    return result


if __name__ == "__main__":
    ticket = Ticket(
        ticket_title="Implement a new feature",
        ticket_body="The feature should allow users to export data in CSV format.",
        ticket_number="12345",
    )
    main(ticket, "")
