from flock.core import FlockAgent
from agents.writer_agent import WriterAgent


def setup_writer_agent() -> FlockAgent:
    writer_agent = WriterAgent(
        name="writer_agent",
    )
    return writer_agent.create_writer_agent()
