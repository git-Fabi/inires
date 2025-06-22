from flock.core import FlockAgent
from src.agents.evaluation_agent import EvaluationAgent


def setup_evaluation_agent() -> FlockAgent:
    """
    Creates and returns a configured EvaluationAgent instance.
    """
    factory = EvaluationAgent(name="evaluation_agent")
    return factory.create_evaluation_agent()
