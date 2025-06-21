from flock.core import FlockFactory, FlockAgent
from src.utils.tools import write_code_to_file


class WriterAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = (
            "You are a programmer that gets a plan to generate a solution "
            "for a ticket. Your task is to write code for this plan and "
            "according to best practices."
        )

    def create_writer_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input="plan: str | The plan to implement the solution for the "
            "ticket. This plan includes the relevant files that should "
            "be modified or created. The plan is a JSON string that "
            "provides a step-by-step guide.",
            output="commit_message: str | A JSON object with a message that "
            "describes the changes made in the code. where they were "
            "made and why.",
            tools=[write_code_to_file],
            temperature=1.0,
            max_tokens=16384,
        )
