from flock.core import FlockFactory, FlockAgent
from src.utils.tools import write_code_to_file, read_code_file


class WriterAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = (
            "You are a genius programmer that writes code based on detailed plans. Your role is to implement solutions and ensure that all necessary files are properly created or modified, without leaving any code incomplete or marked with 'ToDos'. Your goal is to produce production-ready code."
        )

    def create_writer_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input="plan: str | The plan to implement the solution for. ",
            output="commit_message: str | A JSON object with a message that ",
            tools=[write_code_to_file, read_code_file],
            temperature=0.7,
            max_tokens=16384,
        )
