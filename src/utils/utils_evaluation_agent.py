from flock.core import FlockAgent, Flock
import json
from typing import Any, Tuple, Dict, Optional

from src.agents.evaluation_agent import EvaluationAgent

# Constants moved from utils_agents.py to make the evaluation loop self-contained
MAX_EVALUATION_ATTEMPTS = 3
DEFAULT_EVALUATION_THRESHOLD = 8


def setup_evaluation_agent() -> FlockAgent:
    """
    Creates and returns a configured EvaluationAgent instance.
    """
    factory = EvaluationAgent(name="evaluation_agent")
    return factory.create_evaluation_agent()


def run_evaluation_loop(
    flock: Flock,
    repo_context_str: str,
    ticket_context: Dict[str, Any],
    evaluation_threshold: int = DEFAULT_EVALUATION_THRESHOLD,
) -> Tuple[Optional[str], float]:
    """
    Runs the plan generation and evaluation loop to get the best solution plan.

    Args:
        flock: The Flock instance with the registered agents
        repo_context_str: String representation of the repository context
        ticket_context: Dictionary containing the ticket context
        evaluation_threshold: Minimum score threshold to consider a plan acceptable

    Returns:
        Tuple containing (best_plan, best_score), where best_plan may be None if no plan was generated
    """
    best_plan: Optional[str] = None
    best_score: float = -1.0
    feedback = "No feedback yet. This is the first attempt."

    print("\n[3/4] Entering Generation/Evaluation Loop...")

    for attempt in range(MAX_EVALUATION_ATTEMPTS):
        print(f"\n   --- Attempt {attempt + 1}/{MAX_EVALUATION_ATTEMPTS} ---")

        print("   [+] Generating Plan...")
        generator_input = {
            "relevant_files_context": repo_context_str,
            "ticket_context": json.dumps(ticket_context),
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
            score = float(evaluation.get("score", 0.0))
            feedback = evaluation.get("feedback", "No feedback provided.")
        except (ValueError, AttributeError) as e:
            print(f"      -> ERROR: Could not parse evaluation. Retrying. Details: {e}")
            score = 0.0
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

    # Guarantee that we always return a string for best_plan, even if it's empty
    return (best_plan or "{}"), best_score
