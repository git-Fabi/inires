from typing import Any

import pytest

from agents.evaluation_agent import EvaluationAgent
from utils.tools import read_repository_files


class DummyFlockAgent:
    pass


def test_evaluation_agent_initialization() -> None:
    """Test that an EvaluationAgent is initialized with the correct name and null agent."""
    agent = EvaluationAgent(name="test_agent")
    assert agent.name == "test_agent"
    assert agent.agent is None


def test_create_evaluation_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_evaluation_agent calls FlockFactory with correct parameters."""
    agent = EvaluationAgent(name="test_agent")
    dummy_agent = object()

    # Define a mock function to replace the real create_default_agent
    def mock_create_default_agent(**kwargs: Any) -> Any:
        # Test that all required parameters are passed correctly
        assert kwargs["name"] == "test_agent"
        assert "expert software engineering lead" in kwargs["description"]
        assert "evaluate a proposed plan" in kwargs["description"]
        assert "input_data" in kwargs["input"]
        assert "evaluation" in kwargs["output"]
        assert kwargs["temperature"] == 0.5
        assert kwargs["max_tokens"] == 4096
        # Compare by function name instead of identity
        assert kwargs["tools"][0].__name__ == read_repository_files.__name__
        return dummy_agent

    # Apply the monkeypatch to replace the real method with our mock
    monkeypatch.setattr(
        "flock.core.FlockFactory.create_default_agent", mock_create_default_agent
    )

    # Call the method we're testing
    result = agent.create_evaluation_agent()

    # Verify that the method returns the dummy agent and sets it on the object
    assert result is dummy_agent
    assert agent.agent is dummy_agent


def test_read_repository_files_in_tools() -> None:
    """Test that the read_repository_files tool is included in the agent's tools."""
    agent = EvaluationAgent()
    created_agent = agent.create_evaluation_agent()

    # Check that the tools property contains a function with the same name as read_repository_files
    assert hasattr(created_agent, "tools")
    assert any(
        tool.__name__ == read_repository_files.__name__ for tool in created_agent.tools
    )
