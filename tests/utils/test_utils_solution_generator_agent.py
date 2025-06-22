from typing import Tuple, Generator
from unittest.mock import patch, MagicMock

import pytest
from flock.core import FlockAgent

from src.utils.utils_solution_generator_agent import setup_solution_generator_agent


@pytest.fixture
def mock_solution_generator_agent() -> (
    Generator[Tuple[MagicMock, MagicMock, MagicMock], None, None]
):
    """Fixture to create a mock SolutionGeneratorAgent"""
    with patch(
        "src.utils.utils_solution_generator_agent.SolutionGeneratorAgent"
    ) as mock_cls:
        mock_agent = MagicMock(spec=FlockAgent)
        mock_instance = MagicMock()
        mock_instance.create_solution_generator_agent.return_value = mock_agent
        mock_cls.return_value = mock_instance
        yield mock_cls, mock_instance, mock_agent


def test_setup_solution_generator_agent(
    mock_solution_generator_agent: Tuple[MagicMock, MagicMock, MagicMock],
) -> None:
    """Test that setup_solution_generator_agent creates and returns a FlockAgent instance"""
    mock_cls, mock_instance, mock_agent = mock_solution_generator_agent

    # Call the function under test
    result = setup_solution_generator_agent()

    # Verify interactions
    mock_cls.assert_called_once_with(name="solution_generator_agent")
    mock_instance.create_solution_generator_agent.assert_called_once()

    # Verify return value
    assert result is mock_agent


def test_setup_solution_generator_agent_integration() -> None:
    """
    Integration test that checks the actual SolutionGeneratorAgent is created
    without mocking the implementation details
    """
    # This test will create a real agent to verify the function works end-to-end
    agent = setup_solution_generator_agent()

    # Verify the agent type
    assert isinstance(agent, FlockAgent)

    # Verify key attributes
    assert hasattr(agent, "name")
    assert agent.name == "solution_generator_agent"
