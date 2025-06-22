from typing import Optional, Any

from models.ticket import Ticket
from utils.utils_agents import setup_agents, runner


def main(ticket: Ticket, repository: Optional[str] = None) -> Any:
    """
    This is the main execution function.
    It sets up the application, creates test data, and runs the agent pipeline.
    """
    print("--- Setting up Agents ---")
    inires_flock = setup_agents()

    print("--- Kicking off Agent Pipeline ---")
    result = runner(inires_flock, ticket=ticket, repository_input=repository)
    return result


if __name__ == "__main__":
    print("--- Preparing Test Ticket ---")
    sample_ticket = Ticket(
        ticket_title="RestApi with sqlite connection",
        ticket_body=(
            "Create a REST API that connects to a SQLite database. "
            "The API should support basic CRUD operations for a simple resource, "
            "such as 'users' or 'products'. Ensure that the API is well-documented "
            "and includes error handling for common scenarios."
        ),
        ticket_number="TICK-456",
    )

    final_solution_plan = main(sample_ticket)

    print("\n--- FINAL RESULT FROM PIPELINE ---")
    print(final_solution_plan)
    print("----------------------------------")
