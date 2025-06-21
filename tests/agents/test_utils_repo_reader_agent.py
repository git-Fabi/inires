import json
import os
import tempfile
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from flock.core import FlockAgent

from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    _scan_repository_filesystem,
    prepare_repo_reader_input,
)


@pytest.fixture
def mock_repo_reader_agent() -> Generator[MagicMock, None, None]:
    """Fixture that returns a mock agent and patches the create_repo_reader_agent method."""
    mock_agent = MagicMock()
    with patch(
        "src.agents.repo_reader_agent.RepoReaderAgent.create_repo_reader_agent",
        return_value=mock_agent,
    ):
        yield mock_agent


@pytest.fixture
def mock_flock_agent() -> Generator[MagicMock, None, None]:
    """Fixture that returns a mock FlockAgent and patches the create_repo_reader_agent method."""
    mock_agent = MagicMock(spec=FlockAgent)
    with patch(
        "src.agents.repo_reader_agent.RepoReaderAgent.create_repo_reader_agent",
        return_value=mock_agent,
    ):
        yield mock_agent


def test_setup_repo_reader_agent(mock_repo_reader_agent: MagicMock) -> None:
    """Test that setup_repo_reader_agent returns the agent created by RepoReaderAgent."""
    result = setup_repo_reader_agent()
    assert result is mock_repo_reader_agent


def test_setup_repo_reader_agent_type(mock_flock_agent: MagicMock) -> None:
    """Test that the agent returned by setup_repo_reader_agent is of the correct type."""
    result = setup_repo_reader_agent()
    assert isinstance(result, type(mock_flock_agent))


def test_scan_repository_filesystem_ignores_dirs_and_lists_files() -> None:
    """Test that _scan_repository_filesystem ignores certain directories and returns file paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create files and ignored directories
        os.makedirs(os.path.join(tmpdir, "__pycache__"))
        os.makedirs(os.path.join(tmpdir, "node_modules"))
        os.makedirs(os.path.join(tmpdir, "src"))
        file1 = os.path.join(tmpdir, "src", "file1.py")
        file2 = os.path.join(tmpdir, "file2.txt")
        with open(file1, "w") as f:
            f.write("print('hello')")
        with open(file2, "w") as f:
            f.write("test")

        # Should ignore __pycache__ and node_modules
        result = _scan_repository_filesystem(tmpdir)
        assert any("file1.py" in f for f in result)
        assert any("file2.txt" in f for f in result)
        assert not any("__pycache__" in f for f in result)
        assert not any("node_modules" in f for f in result)


@patch("src.utils.utils_repo_reader_agent._scan_repository_filesystem")
def test_prepare_repo_reader_input_formats_prompt(mock_scan: MagicMock) -> None:
    """Test that prepare_repo_reader_input correctly formats the input for the repo reader."""
    # Setup mock
    fake_files = ["foo.py", "bar/baz.py"]
    mock_scan.return_value = fake_files

    # Call function under test
    ticket = "Example bug description."
    result = prepare_repo_reader_input(ticket, repo_root="irrelevant")

    # Assertions
    assert 'Problem Description: "Example bug description."' in result
    assert json.dumps(fake_files, indent=2) in result
    assert "Based on the problem description" in result
