# src/agents/evaluation_agent.py
from flock.core import FlockAgent, FlockFactory

from src.utils.tools import read_repository_files


class EvaluationAgent:
    """
    An agent that evaluates a proposed solution plan.
    """

    def __init__(self, name: str = "evaluation_agent") -> None:
        self.name = name
        self.agent = None

    def create_evaluation_agent(self) -> FlockAgent:
        """
        Creates and configures the FlockAgent for evaluating a solution plan.
        """
        description = (
            "You are an expert software engineering lead. Your task is to evaluate a proposed plan "
            "to solve a software ticket. You will be given the plan, the original problem description, "
            "and a JSON string of relevant file paths. "
            "You MUST use the 'read_repository_files' tool to read the file contents before evaluating the plan. "
            "Your goal is to score the plan on a scale of 1 to 10 "
            "and provide concise, actionable feedback for improvement if the score is low. "
            "A score of 10 means the plan is perfect and ready for implementation. "
            "A score below 8 requires feedback. "
            "Your final output must be ONLY a JSON object with two keys: 'score' (an integer from 1 to 10) "
            "and 'feedback' (a string, which can be empty if the plan is good)."
        )

        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=description,
            input="input_data: dict | A dictionary containing 'plan' (str), 'ticket_context' (str), and 'relevant_files_context' (str, a JSON of file paths).",
            output="evaluation: str | A JSON object with 'score' and 'feedback' keys.",
            temperature=0.5,
            max_tokens=4096,
            tools=[read_repository_files],
        )
        return self.agent
