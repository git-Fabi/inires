import logging
import os
from typing import List
from flock.core import flock_tool
from pathlib import Path

LOGGER = logging.getLogger(__name__)


@flock_tool  # type: ignore
def read_repository_files(file_paths: List[str]) -> str:
    """
    Reads the content of one or more files from the local repository filesystem.
    This tool is essential for fetching the context needed to analyze a problem.
    """
    LOGGER.info(f"Tool 'read_repository_files' called with paths: {file_paths}")
    all_contents = []
    for file_path in file_paths:
        try:
            full_path = os.path.abspath(file_path)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                formatted_content = (
                    f"---\nFile: `{file_path}`\n---\n```\n{content}\n```"
                )
                all_contents.append(formatted_content)
            LOGGER.info(f"Successfully read file: {file_path}")
        except FileNotFoundError:
            error_message = f"---\nFile: `{file_path}`\n---\nError: File not found.\n"
            all_contents.append(error_message)
            LOGGER.warning(f"File not found: {file_path}")
        except Exception as e:
            error_message = f"---\nFile: `{file_path}`\n---\nError: Could not read file. Details: {e}\n"
            all_contents.append(error_message)
            LOGGER.error(f"Error reading file {file_path}: {e}")
    return "\n\n".join(all_contents)


@flock_tool  # type: ignore
def write_code_to_file(file_path: str, code: str) -> None:
    try:
        # Ensure the directory exists
        if not Path(file_path).exists():
            Path(file_path).mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
    except Exception as e:
        raise FileNotFoundError(f"Error writing code to file: {file_path}: {e}")


@flock_tool  # type: ignore
def read_code_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise FileNotFoundError(f"Error writing code to file: {file_path}: {e}")
