# src/main.py
from typing import Optional, Any

from src.models.ticket import Ticket
from src.utils.utils_agents import (
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
    print("--- Preparing Test Ticket ---")
    sample_ticket = Ticket(
        ticket_title="WebUI for Agent Communication",
        ticket_body=(
            "Create a WebUI for this System, that visualizes the communication between each of the agents. Use CSS and a single HTML file to write the code for this task. Make it like an interactive Chat-viewer, where we have the different users, alias agents writing in the chat what they are outputtin"
        ),
        ticket_number="TICK-456",
    )

    # For testing, we can set a high threshold to ensure the loop runs.
    # A threshold of 10 forces the agent to generate a "perfect" plan.
    print("\n--- RUNNING WITH HIGH THRESHOLD (10) TO TEST LOOPING ---")
    final_solution_plan = main(sample_ticket, evaluation_threshold=10)

    print("\n--- FINAL RESULT FROM PIPELINE ---")
    print(final_solution_plan)
    print("----------------------------------")
