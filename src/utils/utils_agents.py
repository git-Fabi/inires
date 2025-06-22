# src/utils/utils_agents.py
import json
from typing import Any

from flock.core import Flock
from src.models.ticket import Ticket
from src.utils.utils_evaluation_agent import setup_evaluation_agent
from src.utils.utils_reader_agent import setup_reader_agent
from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    prepare_repo_reader_input,
)
from src.utils.utils_solution_generator_agent import setup_solution_generator_agent
from src.utils.utils_writer_agent import setup_writer_agent

MODEL = "azure/gpt-4o-mini"
MAX_EVALUATION_ATTEMPTS = 3
DEFAULT_EVALUATION_THRESHOLD = 8


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
    repo_reader_input_str = (
        repository_input
        if repository_input is not None
        else prepare_repo_reader_input(ticket_description)
    )
    repo_reader_output = flock.run(
        "repo_reader_agent", input={"repository+ticket_context": repo_reader_input_str}
    )
    repo_context_str = repo_reader_output.get("relevant_classes", "{}")
    print(f"   -> Output: {repo_context_str}")

    print("\n[3/4] Entering Generation/Evaluation Loop...")
    best_plan = None
    best_score = -1
    feedback = "No feedback yet. This is the first attempt."

    for attempt in range(MAX_EVALUATION_ATTEMPTS):
        print(f"\n   --- Attempt {attempt + 1}/{MAX_EVALUATION_ATTEMPTS} ---")

        print("   [+] Generating Plan...")
        generator_input = {
            "relevant_files_context": repo_context_str,
            "feedback": feedback,
        }
        plan_generation_output = flock.run(
            "solution_generator_agent",
            input=generator_input,
        )
        current_plan_str = plan_generation_output.get("solution_plan", "{}")
        print(f"      -> Generated Plan: {current_plan_str}")

        print("   [+] Evaluating Plan...")
        eval_input = {
            "plan": current_plan_str,
            "ticket_context": json.dumps(ticket_context),
            "relevant_files_context": repo_context_str,
        }
        evaluation_output = flock.run(
            "evaluation_agent", input={"input_data": eval_input}
        )
        evaluation_str = evaluation_output.get("evaluation", "{}")
        print(f"      -> Evaluation: {evaluation_str}")

        try:
            evaluation = json.loads(evaluation_str)
            score = int(evaluation.get("score", 0))
            feedback = evaluation.get("feedback", "No feedback provided.")
        except (ValueError, AttributeError) as e:
            print(f"      -> ERROR: Could not parse evaluation. Retrying. Details: {e}")
            score = 0
            feedback = "The evaluation output was malformed. Please provide a valid JSON with 'score' and 'feedback'."
            continue

        if score > best_score:
            best_score = score
            best_plan = current_plan_str
            print(f"   [+] New best plan found with score: {best_score}")

        if best_score >= evaluation_threshold:
            print(
                f"   [+] Plan approved with score {best_score} (Threshold: {evaluation_threshold}). Exiting loop."
            )
            break
        else:
            print(
                f"   [+] Plan score {score} is below threshold of {evaluation_threshold}. Refining with feedback: {feedback}"
            )

    print(f"\n[4/4] Running WriterAgent with Best Plan (Score: {best_score}/10)...")
    writer_output = flock.run(
        "writer_agent",
        input={"plan": best_plan},
    )
    print(f"   -> Output: {writer_output}")

    print("\n--- AGENT PIPELINE FINISHED ---")
    return writer_output
