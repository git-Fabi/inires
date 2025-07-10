import json
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


@patch("utils.utils_agents.setup_programmer_agent")
@patch("utils.utils_agents.setup_solution_generator_agent")
@patch("utils.utils_agents.setup_evaluation_agent")
@patch("utils.utils_agents.setup_repo_reader_agent")
@patch("utils.utils_agents.setup_ticket_agent")
@patch("utils.utils_agents.Flock")
def test_setup_agents(
    mock_flock_class: MagicMock,
    mock_setup_reader_agent: MagicMock,
    mock_setup_repo_reader_agent: MagicMock,
    mock_setup_evaluation_agent: MagicMock,
    mock_setup_solution_generator_agent: MagicMock,
    mock_setup_writer_agent: MagicMock,
) -> None:
    # Setup mock instances
    mock_flock_instance = MagicMock()
    mock_flock_class.return_value = mock_flock_instance

    mock_reader_agent = MagicMock()
    mock_setup_reader_agent.return_value = mock_reader_agent

    mock_repo_reader_agent = MagicMock()
    mock_setup_repo_reader_agent.return_value = mock_repo_reader_agent

    mock_evaluation_agent = MagicMock()
    mock_setup_evaluation_agent.return_value = mock_evaluation_agent

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
    mock_setup_evaluation_agent.assert_called_once()
    mock_setup_solution_generator_agent.assert_called_once()
    mock_setup_writer_agent.assert_called_once()
    mock_flock_instance.add_agent.assert_has_calls(
        [
            call(mock_reader_agent),
            call(mock_repo_reader_agent),
            call(mock_solution_generator_agent),
            call(mock_evaluation_agent),
            call(mock_writer_agent),
        ]
    )
    assert flock == mock_flock_instance


@patch("utils.utils_agents.Flock.run")
def test_runner(mock_flock_run: MagicMock, mock_ticket: MagicMock) -> None:
    mock_flock = MagicMock()
    mock_flock.run = mock_flock_run
    mock_ticket.title = "Mock Ticket Title"

    ticket_reader_output = {"ticket_context": "something useful"}
    repo_reader_output = {
        "relevant_classes": '{"relevant_files": ["file1.py", "file2.py"]}'
    }
    solution_generator_output = {"solution_plan": '{"plan": ["step1", "step2"]}'}
    evaluation_output = {"evaluation": '{"score": 9, "feedback": ""}'}
    writer_output = {"code": "Generated code based on the plan"}

    # Set the return values for each call
    mock_flock_run.side_effect = [
        ticket_reader_output,
        repo_reader_output,
        solution_generator_output,
        evaluation_output,
        writer_output,
    ]

    result = runner(
        mock_flock,
        mock_ticket,
        repository_input="test repository input",
        evaluation_threshold=9,
    )

    repo_context_str = repo_reader_output["relevant_classes"]
    plan_str = solution_generator_output["solution_plan"]
    ticket_context_json = json.dumps(ticket_reader_output)

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
                    "relevant_files_context": repo_context_str,
                    "ticket_context": ticket_context_json,
                    "feedback": "No feedback yet. This is the first attempt.",
                },
            ),
            call(
                "evaluation_agent",
                input={
                    "input_data": {
                        "plan": plan_str,
                        "ticket_context": ticket_context_json,
                        "relevant_files_context": repo_context_str,
                    }
                },
            ),
            call("writer_agent", input={"plan": plan_str}),
        ]
    )

    assert result == writer_output
