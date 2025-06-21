from flock.core import FlockAgent
from src.agents.solution_generator_agent import SolutionGeneratorAgent


def setup_solution_generator_agent() -> FlockAgent:
    """
    Creates and returns a configured SolutionGeneratorAgent instance.
    This follows the same factory pattern as your other agents.
    """
    factory = SolutionGeneratorAgent(name="solution_generator_agent")
    return factory.create_solution_generator_agent()
