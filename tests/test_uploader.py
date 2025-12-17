"""Unit tests for the NextcloudUploader class."""

from pathlib import Path

import pytest
import requests

from nextcloudcli.uploader import NextcloudUploader


class TestNextcloudUploaderInit:
    """Test NextcloudUploader initialization."""

    def test_init_basic(self, sample_share_url: str) -> None:
        """Test basic initialization without password."""
        uploader = NextcloudUploader(sample_share_url)

        assert uploader.share_url == sample_share_url
        assert uploader.password == ""
        assert uploader.share_token == "TestToken123"
        assert uploader.base_url == "https://cloud.example.com/nextcloud"

    def test_init_with_password(
        self, sample_share_url: str, share_password: str
    ) -> None:
        """Test initialization with password."""
        uploader = NextcloudUploader(sample_share_url, share_password)

        assert uploader.password == share_password

    def test_init_simple_url(self, simple_share_url: str) -> None:
        """Test initialization with simple URL (no /nextcloud path)."""
        uploader = NextcloudUploader(simple_share_url)

        assert uploader.share_token == "SimpleToken"
        assert uploader.base_url == "https://cloud.example.com"


class TestExtractShareToken:
    """Test share token extraction from URLs."""

    def test_extract_token_standard_url(self) -> None:
        """Test extracting token from standard URL."""
        uploader = NextcloudUploader("https://cloud.example.com/s/ABC123")
        assert uploader.share_token == "ABC123"

    def test_extract_token_nextcloud_path(self) -> None:
        """Test extracting token from URL with /nextcloud path."""
        uploader = NextcloudUploader(
            "https://cloud.example.com/nextcloud/s/XYZ789"
        )
        assert uploader.share_token == "XYZ789"

    def test_extract_token_trailing_slash(self) -> None:
        """Test extracting token from URL with trailing slash."""
        uploader = NextcloudUploader("https://cloud.example.com/s/TOKEN/")
        assert uploader.share_token == "TOKEN"

    def test_extract_token_invalid_url(self) -> None:
        """Test that invalid URL raises ValueError."""
        with pytest.raises(ValueError, match="Could not extract share token"):
            NextcloudUploader("https://cloud.example.com/invalid/url")

    def test_extract_token_missing_token(self) -> None:
        """Test that URL without token raises ValueError."""
        with pytest.raises(ValueError, match="Could not extract share token"):
            NextcloudUploader("https://cloud.example.com/s/")


class TestGetBaseUrl:
    """Test base URL extraction."""

    def test_base_url_standard(self) -> None:
        """Test base URL from standard setup."""
        uploader = NextcloudUploader("https://cloud.example.com/s/TOKEN")
        assert uploader.base_url == "https://cloud.example.com"

    def test_base_url_with_nextcloud_path(self) -> None:
        """Test base URL with /nextcloud path."""
        uploader = NextcloudUploader(
            "https://cloud.example.com/nextcloud/s/TOKEN"
        )
        assert uploader.base_url == "https://cloud.example.com/nextcloud"

    def test_base_url_custom_port(self) -> None:
        """Test base URL with custom port."""
        uploader = NextcloudUploader("https://cloud.example.com:8443/s/TOKEN")
        assert uploader.base_url == "https://cloud.example.com:8443"

    def test_base_url_subdirectory(self) -> None:
        """Test base URL with subdirectory."""
        uploader = NextcloudUploader(
            "https://example.com/cloud/nextcloud/s/TOKEN"
        )
        assert (
            uploader.base_url == "https://example.com/cloud/nextcloud"
        )


class TestConstructWebdavUrl:
    """Test WebDAV URL construction."""

    def test_webdav_url_standard(self) -> None:
        """Test WebDAV URL construction for standard setup."""
        uploader = NextcloudUploader("https://cloud.example.com/s/TOKEN")
        expected = "https://cloud.example.com/public.php/webdav/"
        assert uploader.webdav_url == expected

    def test_webdav_url_with_nextcloud_path(self) -> None:
        """Test WebDAV URL with /nextcloud path."""
        uploader = NextcloudUploader(
            "https://cloud.example.com/nextcloud/s/TOKEN"
        )
        expected = "https://cloud.example.com/nextcloud/public.php/webdav/"
        assert uploader.webdav_url == expected


class TestUploadFile:
    """Test file upload functionality."""

    def test_upload_success(
        self,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test successful file upload."""
        uploader = NextcloudUploader(sample_share_url)

        # Mock the requests.put call
        mock_put = mocker.patch("requests.put", return_value=mock_successful_response)

        result = uploader.upload_file(temp_file)

        assert result is True
        mock_put.assert_called_once()

        # Verify the call arguments
        call_args = mock_put.call_args
        assert temp_file.name in str(call_args[0][0])  # URL contains filename
        assert call_args[1]["auth"] == ("TestToken123", "")

    def test_upload_with_password(
        self,
        sample_share_url: str,
        share_password: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload with password."""
        uploader = NextcloudUploader(sample_share_url, share_password)

        mock_put = mocker.patch("requests.put", return_value=mock_successful_response)

        result = uploader.upload_file(temp_file)

        assert result is True
        call_args = mock_put.call_args
        assert call_args[1]["auth"] == ("TestToken123", share_password)

    def test_upload_with_custom_name(
        self,
        sample_share_url: str,
        temp_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test upload with custom remote filename."""
        uploader = NextcloudUploader(sample_share_url)

        mock_put = mocker.patch("requests.put", return_value=mock_successful_response)

        result = uploader.upload_file(temp_file, remote_name="custom_name.txt")

        assert result is True
        call_args = mock_put.call_args
        assert "custom_name.txt" in str(call_args[0][0])

    def test_upload_file_not_found(self, sample_share_url: str) -> None:
        """Test upload with non-existent file."""
        uploader = NextcloudUploader(sample_share_url)

        non_existent_file = Path("/tmp/nonexistent_file_12345.txt")

        with pytest.raises(FileNotFoundError):
            uploader.upload_file(non_existent_file)

    def test_upload_auth_error(
        self,
        sample_share_url: str,
        temp_file: Path,
        mock_auth_error_response,
        mocker,
    ) -> None:
        """Test upload with authentication error."""
        uploader = NextcloudUploader(sample_share_url)

        mocker.patch("requests.put", return_value=mock_auth_error_response)

        result = uploader.upload_file(temp_file)

        assert result is False

    def test_upload_permission_error(
        self,
        sample_share_url: str,
        temp_file: Path,
        mock_permission_error_response,
        mocker,
    ) -> None:
        """Test upload with permission error."""
        uploader = NextcloudUploader(sample_share_url)

        mocker.patch("requests.put", return_value=mock_permission_error_response)

        result = uploader.upload_file(temp_file)

        assert result is False

    def test_upload_network_error(
        self, sample_share_url: str, temp_file: Path, mocker
    ) -> None:
        """Test upload with network error."""
        uploader = NextcloudUploader(sample_share_url)

        mocker.patch(
            "requests.put",
            side_effect=requests.exceptions.ConnectionError("Network error"),
        )

        with pytest.raises(requests.exceptions.RequestException):
            uploader.upload_file(temp_file)

    def test_upload_binary_file(
        self,
        sample_share_url: str,
        temp_binary_file: Path,
        mock_successful_response,
        mocker,
    ) -> None:
        """Test uploading binary file."""
        uploader = NextcloudUploader(sample_share_url)

        mock_put = mocker.patch("requests.put", return_value=mock_successful_response)

        result = uploader.upload_file(temp_binary_file)

        assert result is True
        mock_put.assert_called_once()


class TestConnectionTest:
    """Test connection testing functionality."""

    def test_connection_success(
        self, sample_share_url: str, mock_propfind_response, mocker
    ) -> None:
        """Test successful connection test."""
        uploader = NextcloudUploader(sample_share_url)

        mock_request = mocker.patch(
            "requests.request", return_value=mock_propfind_response
        )

        result = uploader.test_connection()

        assert result is True
        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "PROPFIND"

    def test_connection_with_password(
        self,
        sample_share_url: str,
        share_password: str,
        mock_propfind_response,
        mocker,
    ) -> None:
        """Test connection with password."""
        uploader = NextcloudUploader(sample_share_url, share_password)

        mock_request = mocker.patch(
            "requests.request", return_value=mock_propfind_response
        )

        result = uploader.test_connection()

        assert result is True
        call_args = mock_request.call_args
        assert call_args[1]["auth"] == ("TestToken123", share_password)

    def test_connection_auth_failure(
        self, sample_share_url: str, mock_auth_error_response, mocker
    ) -> None:
        """Test connection test with auth failure."""
        uploader = NextcloudUploader(sample_share_url)

        mocker.patch("requests.request", return_value=mock_auth_error_response)

        result = uploader.test_connection()

        assert result is False

    def test_connection_network_error(
        self, sample_share_url: str, mocker
    ) -> None:
        """Test connection test with network error."""
        uploader = NextcloudUploader(sample_share_url)

        mocker.patch(
            "requests.request",
            side_effect=requests.exceptions.ConnectionError("Network error"),
        )

        result = uploader.test_connection()

        assert result is False
