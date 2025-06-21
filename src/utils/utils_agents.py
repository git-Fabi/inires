from models.ticket import Ticket
from flock.core import Flock
from utils.utils_reader_agent import setup_reader_agent
from src.utils.utils_repo_reader_agent import setup_repo_reader_agent

MODEL = "azure/gpt-4o-mini"


def setup_agents() -> Flock:
    flock: Flock = Flock(model=MODEL, name="inires_flock")
      
    reader_agent = setup_reader_agent()
    flock.add_agent(reader_agent)
    
    repo_reader_agent = setup_repo_reader_agent()
    flock.add_agent(repo_reader_agent)

    return flock


def runner(flock: Flock, ticket: Ticket,  repository_input: str) -> str:
    processed_ticket = flock.run("ticket_reader_agent", input=ticket.to_dict())
    print(processed_ticket)

    repository = {
        "repository+ticket_context": repository_input,
    }
    result = flock.run("repo_reader_agent", input=repository)
    print(f"Generated Context: {result}")
    return "ticket solution"
