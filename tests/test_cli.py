"""Unit tests for the CLI interface."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from nextcloudcli.cli import main


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI test runner.

    Returns:
        CliRunner instance for testing CLI commands
    """
    return CliRunner()


class TestCLIHelp:
    """Test CLI help and version commands."""

    def test_help_command(self, cli_runner: CliRunner) -> None:
        """Test --help flag displays help message."""
        result = cli_runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Upload files to Nextcloud public shares" in result.output
        assert "--share-url" in result.output
        assert "--file" in result.output

    def test_version_command(self, cli_runner: CliRunner) -> None:
        """Test --version flag displays version."""
        result = cli_runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "version 0.1.0" in result.output


class TestCLIMissingArguments:
    """Test CLI behavior with missing required arguments."""

    def test_missing_share_url(
        self, cli_runner: CliRunner, temp_file: Path
    ) -> None:
        """Test error when share URL is missing."""
        result = cli_runner.invoke(main, ["--file", str(temp_file)])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()

    def test_missing_file(
        self, cli_runner: CliRunner, sample_share_url: str
    ) -> None:
        """Test error when file argument is missing."""
        result = cli_runner.invoke(main, ["--share-url", sample_share_url])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()

    def test_nonexistent_file(
        self, cli_runner: CliRunner, sample_share_url: str
    ) -> None:
        """Test error when file does not exist."""
        result = cli_runner.invoke(
            main,
            [
                "--share-url",
                sample_share_url,
                "--file",
                "/tmp/nonexistent_123456.txt",
            ],
        )

        assert result.exit_code != 0
        assert "does not exist" in result.output


class TestCLISuccessfulUpload:
    """Test successful upload scenarios."""

    def test_basic_upload(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test basic successful upload."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main, ["--share-url", sample_share_url, "--file", str(temp_file)]
        )

        assert result.exit_code == 0
        assert "Successfully uploaded" in result.output

    def test_upload_with_password(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        share_password: str,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload with password."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main,
            [
                "--share-url",
                sample_share_url,
                "--file",
                str(temp_file),
                "--password",
                share_password,
            ],
        )

        assert result.exit_code == 0
        assert "Successfully uploaded" in result.output

    def test_upload_with_custom_name(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload with custom remote name."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main,
            [
                "--share-url",
                sample_share_url,
                "--file",
                str(temp_file),
                "--remote-name",
                "custom.txt",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully uploaded" in result.output

    def test_upload_quiet_mode(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload in quiet mode."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main,
            ["--share-url", sample_share_url, "--file", str(temp_file), "--quiet"],
        )

        assert result.exit_code == 0
        # In quiet mode, minimal output

    def test_upload_verbose_mode(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload in verbose mode."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main,
            ["--share-url", sample_share_url, "--file", str(temp_file), "--verbose"],
        )

        assert result.exit_code == 0
        # Verbose mode should show more logging


class TestCLIConnectionTest:
    """Test connection testing functionality."""

    def test_connection_test_success(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_propfind_response,
        mocker,
    ) -> None:
        """Test successful connection test."""
        mocker.patch("requests.request", return_value=mock_propfind_response)

        result = cli_runner.invoke(
            main,
            [
                "--share-url",
                sample_share_url,
                "--file",
                str(temp_file),
                "--test-connection",
            ],
        )

        assert result.exit_code == 0
        assert "Connection successful" in result.output

    def test_connection_test_failure(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_auth_error_response,
        mocker,
    ) -> None:
        """Test failed connection test."""
        mocker.patch("requests.request", return_value=mock_auth_error_response)

        result = cli_runner.invoke(
            main,
            [
                "--share-url",
                sample_share_url,
                "--file",
                str(temp_file),
                "--test-connection",
            ],
        )

        assert result.exit_code == 1
        assert "Connection failed" in result.output


class TestCLIUploadFailures:
    """Test upload failure scenarios."""

    def test_upload_auth_failure(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_auth_error_response,
        mocker,
    ) -> None:
        """Test upload with authentication failure."""
        mocker.patch("requests.put", return_value=mock_auth_error_response)

        result = cli_runner.invoke(
            main, ["--share-url", sample_share_url, "--file", str(temp_file)]
        )

        assert result.exit_code == 1
        assert "Failed to upload" in result.output

    def test_upload_permission_failure(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_permission_error_response,
        mocker,
    ) -> None:
        """Test upload with permission error."""
        mocker.patch("requests.put", return_value=mock_permission_error_response)

        result = cli_runner.invoke(
            main, ["--share-url", sample_share_url, "--file", str(temp_file)]
        )

        assert result.exit_code == 1
        assert "Failed to upload" in result.output

    def test_invalid_share_url(
        self, cli_runner: CliRunner, temp_file: Path
    ) -> None:
        """Test upload with invalid share URL."""
        result = cli_runner.invoke(
            main,
            ["--share-url", "https://invalid.com/not/a/share", "--file", str(temp_file)],
        )

        assert result.exit_code == 1
        # Should show error about invalid URL


class TestCLIShortOptions:
    """Test CLI short option flags."""

    def test_short_options(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test using short option flags."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main, ["-u", sample_share_url, "-f", str(temp_file)]
        )

        assert result.exit_code == 0
        assert "Successfully uploaded" in result.output

    def test_short_verbose_flag(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test -v short flag for verbose."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main, ["-u", sample_share_url, "-f", str(temp_file), "-v"]
        )

        assert result.exit_code == 0

    def test_short_quiet_flag(
        self,
        cli_runner: CliRunner,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test -q short flag for quiet."""
        mocker.patch("requests.put", return_value=mock_successful_response)

        result = cli_runner.invoke(
            main, ["-u", sample_share_url, "-f", str(temp_file), "-q"]
        )

        assert result.exit_code == 0
