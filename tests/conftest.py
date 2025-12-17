"""Pytest configuration and shared fixtures for nextcloudcli tests."""

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def sample_share_url() -> str:
    """Return a sample Nextcloud share URL."""
    return "https://cloud.example.com/nextcloud/s/TestToken123"


@pytest.fixture
def simple_share_url() -> str:
    """Return a simple Nextcloud share URL without nextcloud path."""
    return "https://cloud.example.com/s/SimpleToken"


@pytest.fixture
def share_password() -> str:
    """Return a sample share password."""
    return "test_password_123"


@pytest.fixture
def temp_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary test file.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Yields:
        Path to the temporary test file
    """
    test_file = tmp_path / "test_upload.txt"
    test_file.write_text("This is a test file for upload testing.\n")
    yield test_file
    # Cleanup happens automatically with tmp_path


@pytest.fixture
def temp_binary_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary binary test file.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Yields:
        Path to the temporary binary test file
    """
    test_file = tmp_path / "test_binary.bin"
    test_file.write_bytes(b"\x00\x01\x02\x03\x04\x05" * 100)
    yield test_file


@pytest.fixture
def large_temp_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a large temporary test file (1 MB).

    Args:
        tmp_path: Pytest's temporary directory fixture

    Yields:
        Path to the large temporary test file
    """
    test_file = tmp_path / "large_file.dat"
    # Create 1 MB file
    test_file.write_bytes(b"X" * (1024 * 1024))
    yield test_file


@pytest.fixture
def mock_successful_response(mocker):
    """Mock a successful HTTP response.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked response object with status 201
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.text = ""
    return mock_response


@pytest.fixture
def mock_auth_error_response(mocker):
    """Mock an authentication error response.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked response object with status 401
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    return mock_response


@pytest.fixture
def mock_permission_error_response(mocker):
    """Mock a permission denied response.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked response object with status 403
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    return mock_response


@pytest.fixture
def mock_propfind_response(mocker):
    """Mock a successful PROPFIND response for connection testing.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked response object with status 207
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 207
    mock_response.text = '<?xml version="1.0"?><d:multistatus/>'
    return mock_response
