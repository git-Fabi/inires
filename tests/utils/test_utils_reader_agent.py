from unittest.mock import patch, MagicMock

from utils.utils_reader_agent import setup_reader_agent


@patch("utils.utils_reader_agent.TicketAgent")
def test_setup_reader_agent(mock_issue_reader_agent: MagicMock) -> None:
    # Arrange
    mock_instance = MagicMock()
    mock_issue_reader_agent.return_value = mock_instance
    mock_instance.create_issue_reader_agent.return_value = "mocked_agent"

    # Act
    result = setup_reader_agent()

    # Assert
    mock_issue_reader_agent.assert_called_once_with(name="ticket_reader_agent")
    mock_instance.create_issue_reader_agent.assert_called_once()
    assert result == "mocked_agent"
