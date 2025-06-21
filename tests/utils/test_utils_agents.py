from unittest.mock import MagicMock, patch, call

import pytest

from models.ticket import Ticket
from utils.utils_agents import setup_agents, runner


@pytest.fixture
def mock_ticket() -> MagicMock:
    ticket = MagicMock(spec=Ticket)
    ticket.to_dict.return_value = {
        "ticket_title": "Fix logout issue",
        "ticket_body": "Users get stuck on logout.",
        "ticket_number": "TCK-456",
    }
    return ticket


@patch("utils.utils_agents.setup_writer_agent")
@patch("utils.utils_agents.setup_solution_generator_agent")
@patch("utils.utils_agents.setup_repo_reader_agent")
@patch("utils.utils_agents.setup_reader_agent")
@patch("utils.utils_agents.Flock")
def test_setup_agents(
    mock_flock_class,
    mock_setup_reader_agent,
    mock_setup_repo_reader_agent,
    mock_setup_solution_generator_agent,
    mock_setup_writer_agent,
) -> None:
    # Setup mock instances
    mock_flock_instance = MagicMock()
    mock_flock_class.return_value = mock_flock_instance

    mock_reader_agent = MagicMock()
    mock_setup_reader_agent.return_value = mock_reader_agent

    mock_repo_reader_agent = MagicMock()
    mock_setup_repo_reader_agent.return_value = mock_repo_reader_agent

    mock_solution_generator_agent = MagicMock()
    mock_setup_solution_generator_agent.return_value = mock_solution_generator_agent

    mock_writer_agent = MagicMock()
    mock_setup_writer_agent.return_value = mock_writer_agent

    # Call the function
    flock = setup_agents()

    # Assertions
    mock_flock_class.assert_called_once_with(
        model="azure/gpt-4o-mini", name="inires_flock"
    )
    mock_setup_reader_agent.assert_called_once()
    mock_setup_repo_reader_agent.assert_called_once()
    mock_setup_solution_generator_agent.assert_called_once()
    mock_setup_writer_agent.assert_called_once()
    mock_flock_instance.add_agent.assert_has_calls(
        [
            call(mock_reader_agent),
            call(mock_repo_reader_agent),
            call(mock_solution_generator_agent),
            call(mock_writer_agent),
        ]
    )
    assert flock == mock_flock_instance


@patch("utils.utils_agents.Flock.run")
def test_runner(mock_flock_run: MagicMock, mock_ticket: MagicMock) -> None:
    mock_flock = MagicMock()
    mock_flock.run = mock_flock_run
    mock_ticket.title = "Mock Ticket Title"
    # Set the return values for each call
    mock_flock_run.side_effect = [
        {
            "context": "something useful",
            "description": "Parsed description",
        },  # First call (ticket reader)
        {"relevant_files": ["file1.py", "file2.py"]},  # Second call (repo reader)
        {"plan": ["step1", "step2"]},  # Third call (solution generator)
        {"code": "Generated code based on the plan"},  # Fourth call (writer)
    ]

    result = runner(mock_flock, mock_ticket, repository_input="test repository input")
    mock_flock.run.assert_has_calls(
        [
            call("ticket_reader_agent", input=mock_ticket.to_dict()),
            call(
                "repo_reader_agent",
                input={
                    "repository+ticket_context": "test repository input",
                },
            ),
            call(
                "solution_generator_agent",
                input={
                    "relevant_files_context": {
                        "relevant_files": ["file1.py", "file2.py"]
                    }
                },
            ),
            call("writer_agent", input={"plan": {"plan": ["step1", "step2"]}}),
        ]
    )

    assert result == {"code": "Generated code based on the plan"}
