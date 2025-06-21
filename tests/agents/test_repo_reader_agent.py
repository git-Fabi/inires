from typing import Any
from unittest.mock import MagicMock
import pytest

from src.agents.repo_reader_agent import RepoReaderAgent


class DummyFlockAgent:
    pass


def test_repo_reader_agent_initialization() -> None:
    """Test that the RepoReaderAgent initializes with the correct name and null agent."""
    agent = RepoReaderAgent(name="test_agent")
    assert agent.name == "test_agent"
    assert agent.agent is None


def test_create_repo_reader_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_repo_reader_agent calls FlockFactory with correct parameters."""
    agent = RepoReaderAgent(name="test_agent")
    dummy_instance = DummyFlockAgent()

    def dummy_create_default_agent(**kwargs: Any) -> DummyFlockAgent:
        assert kwargs["name"] == "test_agent"
        assert "analyzes a problem description" in kwargs["description"]
        assert "repository+ticket_context" in kwargs["input"]
        assert "relevant_classes" in kwargs["output"]
        return dummy_instance

    monkeypatch.setattr(
        "flock.core.FlockFactory.create_default_agent", dummy_create_default_agent
    )
    result = agent.create_repo_reader_agent()
    assert result is dummy_instance
    assert agent.agent is dummy_instance
