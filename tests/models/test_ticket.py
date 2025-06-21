from unittest.mock import MagicMock

import pytest
from models.ticket import Ticket


@pytest.fixture
def sample_ticket() -> Ticket:
    return Ticket("Fix login bug", "Login fails on Safari", "TCK-123")


def test_ticket_initialization(sample_ticket: MagicMock) -> None:
    assert sample_ticket.title == "Fix login bug"
    assert sample_ticket.body == "Login fails on Safari"
    assert sample_ticket.number == "TCK-123"


def test_ticket_dict_method(sample_ticket: MagicMock) -> None:
    expected = {
        "ticket_title": "Fix login bug",
        "ticket_body": "Login fails on Safari",
        "ticket_number": "TCK-123",
    }
    assert sample_ticket.to_dict() == expected


def test_get_representation_for_agent() -> None:
    rep = Ticket.get_representation_for_agent()
    assert isinstance(rep, str)
    assert "ticket_title: str" in rep
    assert "ticket_body: str" in rep
    assert "ticket_number: str" in rep
