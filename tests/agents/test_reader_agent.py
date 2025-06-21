from typing import Any, Generator
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from src.agents.reader_agent import IssueReaderAgent


@pytest.fixture
def mock_ticket_and_context() -> (
    Generator[tuple[MagicMock | AsyncMock, MagicMock | AsyncMock], Any, None]
):
    with (
        patch("models.ticket.Ticket.get_representation_for_agent") as mock_ticket_repr,
        patch(
            "models.ticket_context.TicketContext.get_representation_for_agent"
        ) as mock_context_repr,
    ):
        mock_ticket_repr.return_value = "ticket-representation"
        mock_context_repr.return_value = "context-representation"
        yield mock_ticket_repr, mock_context_repr


@pytest.fixture
def mock_flock_factory() -> (
    Generator[tuple[MagicMock | AsyncMock, MagicMock], Any, None]
):
    with patch("flock.core.FlockFactory.create_default_agent") as mock_factory:
        mock_agent = MagicMock(name="FlockAgent")
        mock_factory.return_value = mock_agent
        yield mock_factory, mock_agent


def test_issue_reader_agent_initialization() -> None:
    agent = IssueReaderAgent("Reader1")
    assert agent.name == "Reader1"


def test_create_issue_reader_agent(
    mock_ticket_and_context: MagicMock, mock_flock_factory: MagicMock
) -> None:
    mock_ticket_repr, mock_context_repr = mock_ticket_and_context
    mock_factory, mock_agent = mock_flock_factory

    agent = IssueReaderAgent("Reader2")
    returned_agent = agent.create_issue_reader_agent()

    # Ensure factory is called with correct parameters
    mock_factory.assert_called_once_with(
        name="Reader2",
        description=agent.description,
        input=mock_ticket_repr.return_value,
        output=mock_context_repr.return_value,
        temperature=1.0,
        max_tokens=16384,
    )

    assert returned_agent == mock_agent
