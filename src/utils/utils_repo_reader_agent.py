from src.agents.repo_reader_agent import RepoReaderAgent
from flock.core import FlockAgent


def setup_repo_reader_agent() -> FlockAgent:
    repo_reader_agent = RepoReaderAgent(name="repo_reader_agent")
    return repo_reader_agent.create_repo_reader_agent()
