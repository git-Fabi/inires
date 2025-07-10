from unittest.mock import patch, MagicMock

import pytest

from src.utils.utils_writer_agent import setup_programmer_agent


@pytest.fixture
def mock_writer_agent() -> tuple[MagicMock, MagicMock]:
    mock = MagicMock()
    mock_flock_agent = MagicMock()
    mock.create_programmer_agent.return_value = mock_flock_agent
    return mock, mock_flock_agent


@patch("src.utils.utils_writer_agent.ProgrammerAgent")
def test_setup_writer_agent(
    mock_writer_agent_class: MagicMock, mock_writer_agent: tuple[MagicMock, MagicMock]
) -> None:
    mock_instance, mock_flock_agent = mock_writer_agent
    mock_writer_agent_class.return_value = mock_instance

    result = setup_programmer_agent()

    mock_writer_agent_class.assert_called_once_with(name="programmer_agent")
    mock_instance.create_programmer_agent.assert_called_once()
    assert result == mock_flock_agent
