# src/utils/utils_agents.py
import json
from typing import Any

from flock.core import Flock
from src.models.ticket import Ticket
from src.utils.utils_evaluation_agent import (
    setup_evaluation_agent,
    run_evaluation_loop,
    DEFAULT_EVALUATION_THRESHOLD,
)
from src.utils.utils_reader_agent import setup_reader_agent
from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    prepare_repo_reader_input,
)
from src.utils.utils_solution_generator_agent import setup_solution_generator_agent
from src.utils.utils_writer_agent import setup_writer_agent

MODEL = "azure/gpt-4o-mini"


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

    ticket_context: dict[str, Any]
    if isinstance(ticket_context_output, str):
        ticket_context = json.loads(ticket_context_output)
    else:
        # The agent returns a dictionary directly, so we use it as is.
        ticket_context = ticket_context_output

    # The descriptive text is under the 'ticket_context' key, not 'description'.
    ticket_description = ticket_context.get("ticket_context", ticket.title)

    print("\n[2/4] Running RepoReaderAgent...")
    # Ensure we have a non-empty input string for the repo_reader_agent
    repo_reader_input_str = (
        repository_input
        if repository_input is not None and repository_input != ""
        else prepare_repo_reader_input(ticket_description)
    )

    # Safeguard against empty input
    if not repo_reader_input_str:
        print(
            "   -> WARNING: Empty input for RepoReaderAgent. Generating fallback input."
        )
        repo_reader_input_str = f"Ticket description: {ticket_description}\nPlease identify relevant files for this task."

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
        ticket_context,
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
