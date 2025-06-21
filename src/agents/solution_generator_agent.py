# agents/solution_generator_agent.py
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
        # --- UPDATED DESCRIPTION ---
        # The instructions now explicitly tell the agent about the tool it can use.
        description = (
            "You are an expert software architect AI. Your task is to solve a given software problem. "
            "You will be provided with the problem description and a list of potentially relevant file paths. "
            "To solve the problem, you MUST first use the 'read_repository_files' tool to get the content of those files. "
            "After you have read the files, analyze their content and the problem description to create a clear, "
            "step-by-step, natural-language plan for the fix. "
            "Do NOT write any code. Only create the plan. "
            "Your final output must be ONLY a JSON object with a single key 'plan', "
            "which holds a list of strings. Each string is a single, actionable step."
        )

        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=description,
            # The input will now be the output from the RepoReader agent.
            input="relevant_files_context: str | This is a JSON object from the previous agent containing a list of relevant file paths.",
            output="solution_plan: str | A JSON object with a 'plan' key containing a list of steps.",
            temperature=0.7,
            max_tokens=16384,
            max_tool_calls = 1000,
            tools=[read_repository_files]
        )
        return self.agent