import json
import logging
import os

from flock.core import FlockAgent

from src.agents.repo_reader_agent import RepoReaderAgent


def setup_repo_reader_agent() -> FlockAgent:
    repo_reader_agent = RepoReaderAgent(name="repo_reader_agent")
    return repo_reader_agent.create_repo_reader_agent()


def _scan_repository_filesystem(root_dir: str = ".") -> list[str]:
    """
    Scans the repository from a given root directory to get a list of all file paths.

    This is a helper function that intelligently ignores common non-code directories
    and files to reduce noise and provide a cleaner file list to the LLM.

    Args:
        root_dir: The starting directory to scan (defaults to the current directory).

    Returns:
        A list of strings, where each string is a relative file path.
    """
    file_list = []
    # Define directories and files to ignore to avoid cluttering the prompt.
    ignore_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "env",
        "build",
        "dist",
    }

    logging.info(f"Scanning repository from '{os.path.abspath(root_dir)}'...")

    for root, dirs, files in os.walk(root_dir):
        # This line efficiently prunes the directories to prevent `os.walk` from traversing them.
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(os.path.relpath(file_path, root_dir).replace("\\", "/"))

    logging.info(f"Found {len(file_list)} files in the repository.")
    return file_list


def prepare_repo_reader_input(ticket_description: str, repo_root: str = ".") -> str:
    """
    Prepares the single string input required by the RepoReaderAgent.

    This function orchestrates the process:
    1. Scans the local repository filesystem to get a list of all files.
    2. Formats the ticket description and the file list into a structured prompt.

    Args:
        ticket_description: The problem summary (e.g., from the TicketReaderAgent).
        repo_root: The root directory of the repository checkout. In the GitHub
                   Actions runner, this will simply be the current directory (".").

    Returns:
        A single, formatted string ready to be passed to the RepoReaderAgent's run method.
    """
    # 1. Get the repository context by scanning the filesystem.
    repository_files = _scan_repository_filesystem(repo_root)

    # 2. Format the data into a single, structured string prompt for the agent.
    enhanced_prompt = (
        f'Problem Description: "{ticket_description}"\n\n'
        f"Repository File List:\n{json.dumps(repository_files, indent=2)}\n\n"
        "Based on the problem description, please identify the most relevant files."
    )

    return enhanced_prompt
