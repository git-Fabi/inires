from models.Ticket import Ticket
from utils.utils_agents import runner, setup_agents


def main(ticket: Ticket) -> str:
    inires_flock = setup_agents()
    result = runner(inires_flock, ticket=ticket)
    return result


if __name__ == "__main__":
    ticket = Ticket(
        ticket_title="Implement a new feature",
        ticket_body="The feature should allow users to export data in CSV format.",
        ticket_number="12345",
    )
    main(ticket)
