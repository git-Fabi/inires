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
            "Since you have context about the ticket, your main focus is to make sure that the plan fullfills the requirements of the ticket. "
            "You MUST use the 'read_repository_files' tool to read the file contents before evaluating the plan. "
            "Since you know best, make suggestions to improve the plan if you think it is not good enough. But also make sure to be accepting of plans that are good enough. "
            "Your goal is to score the plan on a scale of 1.0 to 10.0, allowing for fractional scores to better distinguish between plans. "
            "CRITICAL: You MUST explain exactly why you lowered the score and by how much for each issue found. "
            "Start with a perfect 10.0/10.0 score and explicitly deduct points for each flaw. "
            "Use this exact format for scoring breakdown: "
            "'-1.0 because the plan is missing step X that is critical for Y' "
            "'-0.5 because step Z lacks sufficient detail about how to implement feature W' "
            "'-2.0 because the plan incorrectly assumes X when the code actually does Y' "
            "Your feedback MUST include this detailed breakdown showing each deduction and the final calculated score. "
            "Example: 'Starting at 10.0: -1.5 for missing integration step -> -0.5 for unclear file paths -> Final score: 8.0. Please refine integration step and clearify file paths' "
            "Provide concise, specific, and actionable feedback for improvement, especially if the score is low. "
            "Be precise in your scoring, ensuring that it reflects the plan's quality and completeness, whilst using the full scale from 1.0 to 10.0. "
            "Your final output must be ONLY a JSON object with two keys: 'score' (a float from 1.0 to 10.0) "
            "and 'feedback', which must include the detailed score breakdown and specific suggestions for improvement."
        )

        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=description,
            input="input_data: dict | A dictionary containing 'plan' (str), 'ticket_context' (str), and 'relevant_files_context' (str, a JSON of file paths).",
            output="evaluation: str | A JSON object with 'score' (float) and 'feedback' keys.",
            temperature=0.5,
            max_tokens=16384,
            tools=[read_repository_files],
        )
        return self.agent
