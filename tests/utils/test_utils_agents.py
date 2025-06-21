import pytest
from unittest.mock import MagicMock, patch

from models.ticket import Ticket
from utils.utils_agents import setup_agents, runner


@pytest.fixture
def mock_ticket():
    ticket = MagicMock(spec=Ticket)
    ticket.to_dict.return_value = {
        "ticket_title": "Fix logout issue",
        "ticket_body": "Users get stuck on logout.",
        "ticket_number": "TCK-456",
    }
    return ticket


@patch("utils.utils_agents.setup_reader_agent")
@patch("utils.utils_agents.Flock")
def test_setup_agents(mock_flock_class, mock_setup_reader_agent):
    # Setup mock instances
    mock_flock_instance = MagicMock()
    mock_flock_class.return_value = mock_flock_instance

    mock_reader_agent = MagicMock()
    mock_setup_reader_agent.return_value = mock_reader_agent

    # Call the function
    flock = setup_agents()

    # Assertions
    mock_flock_class.assert_called_once_with(
        model="azure/gpt-4o-mini", name="inires_flock"
    )
    mock_setup_reader_agent.assert_called_once()
    mock_flock_instance.add_agent.assert_called_once_with(mock_reader_agent)
    assert flock == mock_flock_instance


@patch("utils.utils_agents.Flock.run")
def test_runner(mock_flock_run, mock_ticket):
    mock_flock = MagicMock()
    mock_flock.run = mock_flock_run
    mock_flock_run.return_value = {"context": "something useful"}

    result = runner(mock_flock, mock_ticket)

    mock_flock_run.assert_called_once_with(
        "ticket_reader_agent", input=mock_ticket.to_dict()
    )
    assert result == "ticket solution"
