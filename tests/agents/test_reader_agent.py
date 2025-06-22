

def test_issue_reader_agent_initialization_empty_name() -> None:
    with pytest.raises(ValueError):
        IssueReaderAgent("")


def test_issue_reader_agent_creation_exception(
    mock_ticket_and_context: Tuple[MagicMock, MagicMock],
    mock_flock_factory: Tuple[MagicMock, MagicMock],
) -> None:
    mock_flock_factory[0].side_effect = Exception("Factory error")
    agent = IssueReaderAgent("Reader3")
    with pytest.raises(Exception):
        agent.create_issue_reader_agent()


def test_issue_reader_agent_invalid_representation(
    mock_ticket_and_context: Tuple[MagicMock, MagicMock],
) -> None:
    mock_ticket_and_context[0].return_value = None  # Simulate invalid representation
    agent = IssueReaderAgent("Reader4")
    with pytest.raises(ValueError):
        agent.create_issue_reader_agent()
