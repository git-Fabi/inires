import pytest
from unittest.mock import patch, MagicMock

from src.agents.writer_agent import WriterAgent


@pytest.fixture
def mock_writer_agent() -> WriterAgent:
    return WriterAgent("test_writer")


def test_writer_agent_initialization(mock_writer_agent: WriterAgent) -> None:
    assert mock_writer_agent.name == "test_writer"


@patch("src.agents.writer_agent.FlockFactory")
def test_create_writer_agent(
    mock_flock_factory: MagicMock, mock_writer_agent: WriterAgent
) -> None:
    mock_flock_agent = MagicMock()
    mock_flock_factory.create_default_agent.return_value = mock_flock_agent

    result = mock_writer_agent.create_writer_agent()

    mock_flock_factory.create_default_agent.assert_called_once()
    assert result == mock_flock_agent
