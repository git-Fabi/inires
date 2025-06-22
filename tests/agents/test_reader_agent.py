def test_issue_reader_agent_error_handling() -> None:
    agent = IssueReaderAgent("Reader4")

    # Simulate unexpected data format
    with pytest.raises(ValueError, match="Invalid input data structure"):
        agent.create_issue_reader_agent()  # This should trigger the error handling

    # You can add more assertions to check for logging or specific behavior.