from typing import Any

import pytest

from src.agents.solution_generator_agent import SolutionGeneratorAgent
from src.utils.tools import read_repository_files


class DummyFlockAgent:
    pass


def test_solution_generator_agent_initialization() -> None:
    """Test that a SolutionGeneratorAgent is initialized with the correct name and null agent."""
    agent = SolutionGeneratorAgent(name="test_agent")
    assert agent.name == "test_agent"
    assert agent.agent is None


def test_create_solution_generator_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_solution_generator_agent calls FlockFactory with correct parameters."""
    agent = SolutionGeneratorAgent(name="test_agent")
    dummy_agent = object()

    # Define a mock function to replace the real create_default_agent
    def mock_create_default_agent(**kwargs: Any) -> Any:
        # Test that all required parameters are passed correctly
        assert kwargs["name"] == "test_agent"
        assert "expert software architect" in kwargs["description"]
        assert "read_repository_files" in kwargs["description"]
        assert "relevant_files_context" in kwargs["input"]
        assert "solution_plan" in kwargs["output"]
        assert kwargs["temperature"] == 0.7
        assert kwargs["max_tokens"] == 16384
        assert kwargs["max_tool_calls"] == 1000
        assert kwargs["tools"] == [read_repository_files]
        return dummy_agent

    # Apply the monkeypatch to replace the real method with our mock
    monkeypatch.setattr(
        "flock.core.FlockFactory.create_default_agent", mock_create_default_agent
    )

    # Call the method we're testing
    result = agent.create_solution_generator_agent()

    # Verify that the method returns the dummy agent and sets it on the object
    assert result is dummy_agent
    assert agent.agent is dummy_agent


def test_read_repository_files_in_tools() -> None:
    """Test that the read_repository_files tool is included in the agent's tools."""
    agent = SolutionGeneratorAgent()
    created_agent = agent.create_solution_generator_agent()

    # Check that the tools property contains our read_repository_files function
    assert hasattr(created_agent, "tools")
    assert read_repository_files in created_agent.tools
