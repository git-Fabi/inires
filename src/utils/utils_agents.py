from flock.core import Flock

from src.utils.utils_repo_reader_agent import setup_repo_reader_agent

MODEL = "azure/gpt-4o-mini"


def setup_agents() -> Flock:
    flock: Flock = Flock(model=MODEL, name="inires_flock")
    repo_reader_agent = setup_repo_reader_agent()
    flock.add_agent(repo_reader_agent)

    return flock


def runner(flock: Flock, repository_input: str):

    repository = {
        "repository+ticket_context": repository_input,
    }
    result = flock.run("repo_reader_agent", input=repository)
    print(f"Generated Context: {result}")
    return "Repo Context"
