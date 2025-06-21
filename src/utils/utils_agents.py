import json

from flock.core import Flock
from typing import Any
from models.ticket import Ticket
from src.utils.utils_reader_agent import setup_reader_agent
from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    prepare_repo_reader_input,
)

# This import is now clean and won't cause a circle
from src.utils.utils_solution_generator_agent import setup_solution_generator_agent
from utils.utils_writer_agent import setup_writer_agent

# This import now points to the new, dedicated tools file

MODEL = "azure/gpt-4o-mini"


def setup_agents() -> Flock:
    """Sets up the Flock instance with all agents and tools."""
    flock: Flock = Flock(model=MODEL, name="inires_flock")

    # Add all three agents
    flock.add_agent(setup_reader_agent())
    flock.add_agent(setup_repo_reader_agent())
    flock.add_agent(setup_solution_generator_agent())
    flock.add_agent(setup_writer_agent())

    return flock


def runner(flock: Flock, ticket: Ticket, repository_input: str = "") -> Any:
    print("--- STARTING AGENT PIPELINE ---")

    print("\n[1/4] Running TicketReaderAgent...")
    ticket_context_json = flock.run("ticket_reader_agent", input=ticket.to_dict())
    print(f"   -> Output: {ticket_context_json}")
    if isinstance(ticket_context_json, str):
        ticket_description = json.loads(ticket_context_json).get(
            "description", ticket.title
        )
    else:
        ticket_description = ticket_context_json.get("description", ticket.title)

    print("\n[2/4] Running RepoReaderAgent...")
    repo_reader_input_str = (
        repository_input
        if repository_input
        else prepare_repo_reader_input(ticket_description)
    )
    repo_reader_output_json = flock.run(
        "repo_reader_agent", input={"repository+ticket_context": repo_reader_input_str}
    )
    print(f"   -> Output: {repo_reader_output_json}")

    print("\n[3/4] Running SolutionGeneratorAgent...")
    solution_plan_json = flock.run(
        "solution_generator_agent",
        input={"relevant_files_context": repo_reader_output_json},
    )
    print(f"   -> Final Plan: {solution_plan_json}")

    print("\n[4/4] Running SolutionGeneratorAgent...")
    generated_code = flock.run(
        "writer_agent",
        input={"plan": solution_plan_json},
    )
    print(f"   -> Plan as Code: {generated_code.code}")

    print("\n--- AGENT PIPELINE FINISHED ---")
    return solution_plan_json
