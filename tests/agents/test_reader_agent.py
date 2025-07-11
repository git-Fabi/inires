from typing import Generator, Tuple
from unittest.mock import MagicMock, patch

import pytest

from agents.ticket_agent import TicketAgent


@pytest.fixture
def mock_ticket_and_context() -> Generator[Tuple[MagicMock, MagicMock], None, None]:
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
def mock_flock_factory() -> Generator[Tuple[MagicMock, MagicMock], None, None]:
    with patch("flock.core.FlockFactory.create_default_agent") as mock_factory:
        mock_agent = MagicMock(name="FlockAgent")
        mock_factory.return_value = mock_agent
        yield mock_factory, mock_agent


def test_issue_reader_agent_initialization() -> None:
    agent = TicketAgent("Reader1")
    assert agent.name == "Reader1"


def test_create_issue_reader_agent(
    mock_ticket_and_context: Tuple[MagicMock, MagicMock],
    mock_flock_factory: Tuple[MagicMock, MagicMock],
) -> None:
    mock_ticket_repr, mock_context_repr = mock_ticket_and_context
    mock_factory, mock_agent = mock_flock_factory

    agent = TicketAgent("Reader2")
    returned_agent = agent.create_ticket_agent()

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
