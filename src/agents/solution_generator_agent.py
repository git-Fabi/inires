# src/agents/solution_generator_agent.py
from flock.core import FlockAgent, FlockFactory

from src.utils.tools import read_repository_files


class SolutionGeneratorAgent:
    """
    An agent that generates a solution plan for a given software problem.
    """

    def __init__(self, name: str = "solution_generator_agent") -> None:
        self.name = name
        self.agent = None

    def create_solution_generator_agent(self) -> FlockAgent:
        """
        Creates and configures the FlockAgent for generating a solution plan.
        """
        description = (
            "You are an expert software architect AI. Your task is to solve a given software problem by creating a step-by-step plan. "
            "You will be provided with the ticket context, relevant file paths and, crucially, feedback on your previous plan if it was inadequate. "
            "If feedback is provided (i.e., it is not the first attempt), you MUST use it to refine your plan, rather than writing a complete new one. "
            "Your primary goal is to create a clear, step-by-step, natural-language plan, that could be executed by an AI programmer. Label each step with a number, "
            "This plan shall be oriented towards implementing a solution for the ticket."
            "You MUST use the 'read_repository_files' tool to read the contents of the files. "
            "For each step in the plan that involves a file modification, you MUST specify the full absolute file path. "
            "Do NOT write any code. Only create the plan. "
            "Your final output must be ONLY a JSON object with a single key 'plan', "
            "which holds a list of strings. Each string is a single, actionable step."
            "Your plan should be detailed, but concise."
        )

        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=description,
            input="relevant_files_context: str, ticket_context: str, feedback: str | A JSON string of file paths, the ticket context, and an optional string with feedback for refinement.",
            output="solution_plan: str | A JSON object with a 'plan' key containing a list of steps.",
            temperature=0.7,
            max_tokens=16384,
            max_tool_calls=1000,
            tools=[read_repository_files],
        )
        return self.agent
