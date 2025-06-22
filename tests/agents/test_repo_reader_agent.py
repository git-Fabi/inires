

def test_repo_reader_agent_null_input() -> None:
    with pytest.raises(ValueError):
        RepoReaderAgent(name=None)


def test_repo_reader_agent_no_relevant_files() -> None:
    agent = RepoReaderAgent(name="test_agent")
    agent.relevant_files = []  # Simulate no relevant files
    result = agent.create_repo_reader_agent()
    assert result is None  # Expecting None or appropriate handling


def test_repo_reader_agent_invalid_input_format() -> None:
    agent = RepoReaderAgent(name="test_agent")
    with pytest.raises(ValueError):
        agent.create_repo_reader_agent(input_format='invalid_format')  # Simulating invalid input format
