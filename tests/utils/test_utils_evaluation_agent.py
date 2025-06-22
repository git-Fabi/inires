from typing import Generator
from unittest.mock import patch, MagicMock

import pytest
from flock.core import FlockAgent

from src.utils.utils_evaluation_agent import setup_evaluation_agent


@pytest.fixture
def mock_evaluation_agent() -> Generator[MagicMock, None, None]:
    """Fixture that returns a mock agent and patches the create_evaluation_agent method."""
    mock_agent = MagicMock()
    with patch(
        "src.agents.evaluation_agent.EvaluationAgent.create_evaluation_agent",
        return_value=mock_agent,
    ):
        yield mock_agent


@pytest.fixture
def mock_flock_agent() -> Generator[MagicMock, None, None]:
    """Fixture that returns a mock FlockAgent and patches the create_evaluation_agent method."""
    mock_agent = MagicMock(spec=FlockAgent)
    with patch(
        "src.agents.evaluation_agent.EvaluationAgent.create_evaluation_agent",
        return_value=mock_agent,
    ):
        yield mock_agent


def test_setup_evaluation_agent(mock_evaluation_agent: MagicMock) -> None:
    """Test that setup_evaluation_agent returns the agent created by EvaluationAgent."""
    result = setup_evaluation_agent()
    assert result is mock_evaluation_agent


def test_setup_evaluation_agent_type(mock_flock_agent: MagicMock) -> None:
    """Test that the agent returned by setup_evaluation_agent is of the correct type."""
    result = setup_evaluation_agent()
    assert isinstance(result, type(mock_flock_agent))


@patch("src.utils.utils_evaluation_agent.EvaluationAgent")
def test_setup_evaluation_agent_initialization(
    mock_evaluation_agent_class: MagicMock,
) -> None:
    """Test that the EvaluationAgent is initialized with the correct name."""
    # Arrange
    mock_instance = MagicMock()
    mock_evaluation_agent_class.return_value = mock_instance
    mock_instance.create_evaluation_agent.return_value = "mocked_agent"

    # Act
    result = setup_evaluation_agent()

    # Assert
    mock_evaluation_agent_class.assert_called_once_with(name="evaluation_agent")
    mock_instance.create_evaluation_agent.assert_called_once()
    assert result == "mocked_agent"
