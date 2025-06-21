from flock.core import FlockAgent

from agents.repo_reader_agent import RepoReaderAgent
from src.utils.utils_repo_reader_agent import setup_repo_reader_agent


class DummyFlockAgent:
    pass


def test_setup_repo_reader_agent(monkeypatch):
    dummy_agent = DummyFlockAgent()

    def dummy_create_repo_reader_agent(self):
        return dummy_agent

    monkeypatch.setattr(
        RepoReaderAgent, "create_repo_reader_agent", dummy_create_repo_reader_agent
    )
    result = setup_repo_reader_agent()
    assert result is dummy_agent


def test_setup_repo_reader_agent_type(monkeypatch):
    class DummyFlockAgent(FlockAgent):
        pass

    def dummy_create_repo_reader_agent(self):
        return DummyFlockAgent("dummy")

    monkeypatch.setattr(
        RepoReaderAgent, "create_repo_reader_agent", dummy_create_repo_reader_agent
    )
    result = setup_repo_reader_agent()
    assert isinstance(result, FlockAgent)
