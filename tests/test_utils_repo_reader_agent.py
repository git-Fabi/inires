import json
import os
import tempfile

from flock.core import FlockAgent

from src.agents.repo_reader_agent import RepoReaderAgent
from src.utils.utils_repo_reader_agent import (
    setup_repo_reader_agent,
    _scan_repository_filesystem,
    prepare_repo_reader_input,
)


class DummyFlockAgent:
    pass


def test_setup_repo_reader_agent(monkeypatch):
    dummy_agent = DummyFlockAgent()

    def dummy_create_repo_reader_agent(self):
        return dummy_agent

    monkeypatch.setattr(
        "src.agents.repo_reader_agent.RepoReaderAgent.create_repo_reader_agent",
        dummy_create_repo_reader_agent,
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


def test_scan_repository_filesystem_ignores_dirs_and_lists_files():
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


def test_prepare_repo_reader_input_formats_prompt(monkeypatch):
    ticket = "Example bug description."
    fake_files = ["foo.py", "bar/baz.py"]

    def fake_scan(_):
        return fake_files

    monkeypatch.setattr(
        "src.utils.utils_repo_reader_agent._scan_repository_filesystem", fake_scan
    )
    result = prepare_repo_reader_input(ticket, repo_root="irrelevant")
    assert 'Problem Description: "Example bug description."' in result
    assert json.dumps(fake_files, indent=2) in result
    assert "Based on the problem description" in result
