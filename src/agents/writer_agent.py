from flock.core import FlockFactory, FlockAgent
from src.utils.tools import write_code_to_file, read_code_file


class ProgrammerAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = """
        You are a senior software engineer agent tasked with writing complete, production-ready code based on a detailed implementation plan provided by another agent.
        
        Your responsibilities:
        - Accurately implement the plan as clean, well-structured, and maintainable code.
        - Create or update all necessary files. Do not leave placeholders, partial logic, or 'TODO' comments.
        - Follow established best practices for style, modularity, naming, and documentation.
        - Include unit tests or usage examples where relevant to ensure correctness.
        - Ensure your code integrates cleanly into an existing project structure if applicable.
        - If any part of the plan is unclear or incomplete, make minimal, reasonable assumptions and proceed confidently.
        
        Only output the final code, ready for direct use in a production environment.
        """

    def create_programmer_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input="plan: str | The plan to implement the solution for. ",
            output="commit_message: str | A JSON object with a message that ",
            tools=[write_code_to_file, read_code_file],
            temperature=0.7,
            max_tokens=16384,
        )
