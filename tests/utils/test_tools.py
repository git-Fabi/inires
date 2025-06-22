from pathlib import Path
from typing import Generator
from unittest.mock import patch, MagicMock

import pytest

from src.utils.tools import read_repository_files, write_code_to_file, read_code_file


@pytest.fixture
def mock_open_file() -> Generator[MagicMock, None, None]:
    """Fixture to create mock file content"""
    with patch("builtins.open") as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = "test file content"
        mock_open.return_value.__enter__.return_value = mock_file
        yield mock_open


@pytest.fixture
def mock_isfile() -> Generator[MagicMock, None, None]:
    """Fixture to simulate file existence checks"""
    with patch("os.path.isfile", return_value=True) as mock:
        yield mock


@pytest.fixture
def mock_os_path_abspath() -> Generator[MagicMock, None, None]:
    """Fixture to mock os.path.abspath"""
    with patch("os.path.abspath") as mock:
        mock.side_effect = lambda x: f"/absolute/path/to/{x}"
        yield mock


def test_read_repository_files_success(
    mock_open_file: MagicMock, mock_isfile: MagicMock, mock_os_path_abspath: MagicMock
) -> None:
    """Test that read_repository_files correctly reads file content"""
    # Test with a single file
    result = read_repository_files(["file1.py"])

    # Check that the file was opened
    mock_open_file.assert_called_once()

    # Check that the content was formatted correctly
    assert "File: `file1.py`" in result
    assert "test file content" in result


def test_read_repository_files_multiple_files(
    mock_open_file: MagicMock, mock_isfile: MagicMock, mock_os_path_abspath: MagicMock
) -> None:
    """Test that read_repository_files can handle multiple files"""
    result = read_repository_files(["file1.py", "file2.py"])

    # Should open two files
    assert mock_open_file.call_count == 2

    # Results should contain both files
    assert "File: `file1.py`" in result
    assert "File: `file2.py`" in result


def test_read_repository_files_file_not_found(mock_os_path_abspath: MagicMock) -> None:
    """Test handling of FileNotFoundError"""
    with patch("builtins.open") as mock_open:
        mock_open.side_effect = FileNotFoundError("File not found")

        result = read_repository_files(["nonexistent.py"])

        # Check that the error is formatted correctly
        assert "File: `nonexistent.py`" in result
        assert "Error: File not found" in result


def test_read_repository_files_other_error(mock_os_path_abspath: MagicMock) -> None:
    """Test handling of other errors"""
    with patch("builtins.open") as mock_open:
        mock_open.side_effect = PermissionError("Permission denied")

        result = read_repository_files(["protected.py"])

        # Check that the error is formatted correctly
        assert "File: `protected.py`" in result
        assert "Error: Could not read file" in result
        assert "Permission denied" in result


def test_write_code_to_file_success(tmp_path: Path) -> None:
    file_path = tmp_path / "subdir" / "test_file.py"
    code = "print('Hello, world!')"

    write_code_to_file(str(file_path), code)

    # Read back to confirm write
    with open(file_path, "r", encoding="utf-8") as f:
        assert f.read() == code


def test_write_code_to_file_creates_directory(tmp_path: Path) -> None:
    file_path = tmp_path / "nested" / "dir" / "file.py"
    code = "# auto-generated"

    write_code_to_file(str(file_path), code)

    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        assert f.read() == code


def test_write_code_to_file_raises_file_error() -> None:
    with patch("builtins.open", side_effect=PermissionError("No write access")):
        with pytest.raises(FileNotFoundError) as exc_info:
            write_code_to_file("some/file.py", "data")
        assert "Error writing code to file" in str(exc_info.value)
        assert "No write access" in str(exc_info.value)


def test_read_code_file_success(tmp_path: Path) -> None:
    file_path = tmp_path / "script.py"
    content = "print('hello')"
    file_path.write_text(content, encoding="utf-8")

    result = read_code_file(str(file_path))

    assert result == content


def test_read_code_file_raises_file_error() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError("Missing file")):
        with pytest.raises(FileNotFoundError) as exc_info:
            read_code_file("nonexistent.py")
        assert "Error reading code file" in str(exc_info.value)
        assert "Missing file" in str(exc_info.value)
