from flock.core import FlockAgent
from agents.reader_agent import IssueReaderAgent


def setup_reader_agent() -> FlockAgent:
    reader_agent = IssueReaderAgent(
        name="ticket_reader_agent",
    )
    return reader_agent.create_issue_reader_agent()
