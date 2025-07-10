from flock.core import FlockAgent
from agents.writer_agent import ProgrammerAgent


def setup_programmer_agent() -> FlockAgent:
    programmer_agent = ProgrammerAgent(
        name="programmer_agent",
    )
    return programmer_agent.create_programmer_agent()
