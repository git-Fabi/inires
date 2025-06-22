from flock.core import FlockFactory, FlockAgent
from src.utils.tools import write_code_to_file, read_code_file
import subprocess


class WriterAgent:
    """
    A class representing a reader agent that can read and process text.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.description = (
            "You are a genius programmer and you receive a plan to generate a solution "
            "for a ticket. Your task is to write code for this plan and "
            "resolve the ticket. You write your changes to files in the repository. "
            "The file might not exist, in which case you should create it, but check first. "
            "Whenever you write code inside of an existing file, make sure to write the whole code and dont leave any code out or 'ToDos' "
            "After you are done writing the code, the code / files need to be ready to be used in production. "
        )

    def create_writer_agent(self) -> FlockAgent:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input="plan: str | The plan to implement the solution for. ",
            output="commit_message: str | A JSON object with a message that "
            "describes the changes made in the code. where they were "
            "made and why.",
            tools=[write_code_to_file, read_code_file],
            temperature=0.7,
            max_tokens=16384,
        )

    def git_revert(self, commit_hash: str) -> str:
        """
        Reverts a given commit by executing the git revert command.
        """
        try:
            result = subprocess.run(['git', 'revert', commit_hash], check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr

    def check_set_upstream(self) -> str:
        """
        Checks the effectiveness of the '--set-upstream' option by attempting to push changes.
        """
        try:
            result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'branch_name'], check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr
        
        # Attempt to push without --set-upstream
        try:
            result = subprocess.run(['git', 'push', 'origin', 'branch_name'], check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr
