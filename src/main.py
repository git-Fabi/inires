import argparse

from typing import Optional, Any

from models.ticket import Ticket
from utils.utils_agents import (
    setup_agents,
    runner,
    DEFAULT_EVALUATION_THRESHOLD,
)


def main(
    ticket: Ticket,
    repository: Optional[str] = None,
    evaluation_threshold: int = DEFAULT_EVALUATION_THRESHOLD,
) -> Any:
    """
    This is the main execution function.
    It sets up the application, creates test data, and runs the agent pipeline.
    """
    print("--- Setting up Agents ---")
    inires_flock = setup_agents()

    print("--- Kicking off Agent Pipeline ---")
    result = runner(
        inires_flock,
        ticket=ticket,
        repository_input=repository or "",
        evaluation_threshold=evaluation_threshold,
    )
    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Inires Agent Pipeline")
    parser.add_argument(
        "--ticket-number", type=str, required=False, help="Ticket ID to process"
    )
    parser.add_argument(
        "--ticket-title", type=str, required=False, help="Title of the ticket"
    )
    parser.add_argument(
        "--ticket-body", type=str, required=False, help="Body of the ticket"
    )
    args = parser.parse_args()
    ticket = Ticket(
        ticket_number="2222",
        ticket_title="Create User Interface",
        ticket_body="Create a WebUI for this System, that visualizes the communication between each of the agents. Use CSS and a single HTML file to write the code for this task. Make it like an interactive Chat-viewer, where we have the different users, alias agents writing in the chat what they are outputtin",
    )
    final_solution_plan = main(ticket=ticket, evaluation_threshold=10)
