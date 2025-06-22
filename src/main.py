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
        "--ticket-number", type=str, required=True, help="Ticket ID to process"
    )
    parser.add_argument(
        "--ticket-title", type=str, required=True, help="Title of the ticket"
    )
    parser.add_argument(
        "--ticket-body", type=str, required=True, help="Body of the ticket"
    )
    args = parser.parse_args()
    ticket = Ticket(
        ticket_number=args.ticket_number,
        ticket_title=args.ticket_title,
        ticket_body=args.ticket_body,
    )
    final_solution_plan = main(ticket=ticket, evaluation_threshold=10)
