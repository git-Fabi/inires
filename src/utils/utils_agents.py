from typing import Any

from flock.core import Flock
from src.models.ticket import Ticket
from src.utils.utils_evaluation_agent import (
    setup_evaluation_agent,
    run_evaluation_loop,
    DEFAULT_EVALUATION_THRESHOLD,  # Re-export this constant
)
from src.utils.utils_reader_agent import setup_reader_agent
from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    prepare_repo_reader_input,
)
from src.utils.utils_solution_generator_agent import setup_solution_generator_agent
from src.utils.utils_writer_agent import setup_writer_agent

MODEL = "azure/gpt-4o-mini"

# Re-export the constant so it can be imported from this module
__all__ = ["setup_agents", "runner", "DEFAULT_EVALUATION_THRESHOLD"]


def setup_agents() -> Flock:
    """Sets up the Flock instance with all agents and tools."""
    flock: Flock = Flock(model=MODEL, name="inires_flock")

    # Add all agents
    flock.add_agent(setup_reader_agent())
    flock.add_agent(setup_repo_reader_agent())
    flock.add_agent(setup_solution_generator_agent())
    flock.add_agent(setup_evaluation_agent())
    flock.add_agent(setup_writer_agent())

    return flock


def runner(
    flock: Flock,
    ticket: Ticket,
    repository_input: str = "",
    evaluation_threshold: int = DEFAULT_EVALUATION_THRESHOLD,
) -> Any:
    print("--- STARTING AGENT PIPELINE ---")

    print("\n[1/4] Running TicketReaderAgent...")
    ticket_context_output = flock.run("ticket_reader_agent", input=ticket.to_dict())
    print(f"   -> Output: {ticket_context_output}")

    ticket_context_json = flock.run("ticket_reader_agent", input=ticket.to_dict())
    print(f"   -> Output: {ticket_context_json}")

    print("\n[2/4] Running RepoReaderAgent...")
    # Ensure we have a non-empty input string for the repo_reader_agent
    repo_reader_input_str = (
        repository_input
        if repository_input is not None and repository_input != ""
        else prepare_repo_reader_input(ticket_context_json)
    )

    # Safeguard against empty input
    if not repo_reader_input_str:
        print(
            "   -> WARNING: Empty input for RepoReaderAgent. Generating fallback input."
        )
        repo_reader_input_str = f"Ticket description: {ticket_context_json}\nPlease identify relevant files for this task."

    # Use the original parameter name "repository+ticket_context" that the agent expects
    repo_reader_output = flock.run(
        "repo_reader_agent", input={"repository+ticket_context": repo_reader_input_str}
    )
    print(f"   -> Output: {repo_reader_output}")

    # Extract the relevant_classes string from the output
    repo_context_str = repo_reader_output.get("relevant_classes", "{}")

    # Run the evaluation loop to get the best plan
    best_plan, best_score = run_evaluation_loop(
        flock,
        repo_context_str,
        ticket_context_json,
        evaluation_threshold,
    )

    print(f"\n[4/4] Running WriterAgent with Best Plan (Score: {best_score}/10)...")
    writer_output = flock.run(
        "writer_agent",
        input={"plan": best_plan},
    )
    print(f"   -> Output: {writer_output}")

    print("\n--- AGENT PIPELINE FINISHED ---")
    return writer_output
