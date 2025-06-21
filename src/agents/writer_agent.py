from flock.core import FlockFactory, FlockAgent


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
            input="plan: str | The plan to implement the solution for the " "ticket.",
            output="code: str | The code that implements the solution for the ticket.",
            temperature=1.0,
            max_tokens=16384,
        )
