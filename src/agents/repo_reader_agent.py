# src/agents/repo_reader_agent.py
from flock.core import FlockAgent, FlockFactory


class RepoReaderAgent:
    """
    An agent that reads a repository and returns the most relevant files.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.agent = None

    def create_repo_reader_agent(self) -> FlockAgent:
        """
        Creates and configures the FlockAgent for reading the repository context.

        Uses FlockFactory to build an agent with a specific description that
        defines its role and expected output format.

        Returns:
            The configured FlockAgent instance.
        """
        # This description defines the agent's behavior, matching the parameter
        # used in your IssueReaderAgent example.
        description = (
            "You are an expert programmer, hired to analyze a problem description and a provide list of file paths. "
            "Your goal is to identify a comprehensive list of files that might be relevant for solving the problem. "
            "It's better to include a file that might not be relevant than to miss an important one, so be thorough and consider all files. "
            "Consider not only the core logic files but also tests, documentation, and configuration files that might be affected. "
            "The final output must be ONLY a JSON object containing a single key 'relevant_files' "
            "which holds a list of file path strings."
        )

        self.agent = FlockFactory.create_default_agent(
            name=self.name,
            description=description,
            # The agent's input is a string (problem + file list).
            input="repository+ticket_context: str | This is the repository context and ticket context formatted as a json file, that you will read to evaluate relevant classes.",
            # The agent's output is a string (the JSON result).
            output="relevant_classes: str | This is a JSON object with a single key 'relevant_files' that contains a list of file path strings.",
            temperature=1.0,
            max_tokens=16384,
        )
        return self.agent
