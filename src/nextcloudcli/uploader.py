"""Nextcloud file upload functionality using WebDAV API."""

import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests

logger = logging.getLogger(__name__)


class NextcloudUploader:
    """Upload files to Nextcloud public shares via WebDAV."""

    def __init__(self, share_url: str, password: Optional[str] = None) -> None:
        """Initialize the uploader with share URL and optional password.

        Args:
            share_url: The public share URL (e.g., https://cloud.example.com/s/TOKEN)
            password: Optional password for password-protected shares
        """
        self.share_url = share_url
        self.password = password or ""
        self.share_token = self._extract_share_token(share_url)
        self.base_url = self._get_base_url(share_url)
        self.webdav_url = self._construct_webdav_url(self.base_url)

        logger.debug(f"Initialized uploader for share: {self.share_token}")
        logger.debug(f"WebDAV URL: {self.webdav_url}")

    def _extract_share_token(self, share_url: str) -> str:
        """Extract the share token from the share URL.

        Args:
            share_url: The public share URL

        Returns:
            The extracted share token

        Raises:
            ValueError: If the share token cannot be extracted
        """
        # Parse URL and extract the last part after /s/
        parsed = urlparse(share_url)
        path_parts = parsed.path.rstrip("/").split("/")

        # Find 's' in path and get the token after it
        try:
            s_index = path_parts.index("s")
            token = path_parts[s_index + 1]
            logger.debug(f"Extracted share token: {token}")
            return token
        except (ValueError, IndexError):
            raise ValueError(f"Could not extract share token from URL: {share_url}")

    def _get_base_url(self, share_url: str) -> str:
        """Get the base URL of the Nextcloud instance.

        Args:
            share_url: The public share URL

        Returns:
            The base URL (e.g., https://cloud.example.com)
        """
        parsed = urlparse(share_url)
        # Get everything up to /s/ or /nextcloud/s/
        path = parsed.path.rstrip("/")
        if "/s/" in path:
            path = path[: path.rfind("/s/")]
        base_url = f"{parsed.scheme}://{parsed.netloc}{path}"
        logger.debug(f"Base URL: {base_url}")
        return base_url

    def _construct_webdav_url(self, base_url: str) -> str:
        """Construct the WebDAV URL for public share uploads.

        Args:
            base_url: The base URL of the Nextcloud instance

        Returns:
            The WebDAV URL for uploading files
        """
        # Ensure base_url ends with / for proper urljoin behavior
        if not base_url.endswith("/"):
            base_url = base_url + "/"
        return urljoin(base_url, "public.php/webdav/")

    def upload_file(self, file_path: Path, remote_name: Optional[str] = None) -> bool:
        """Upload a file to the Nextcloud share.

        Args:
            file_path: Path to the local file to upload
            remote_name: Optional remote filename (defaults to local filename)

        Returns:
            True if upload was successful, False otherwise

        Raises:
            FileNotFoundError: If the local file does not exist
            requests.exceptions.RequestException: If the upload request fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use the original filename if no remote name is specified
        target_name = remote_name or file_path.name
        upload_url = urljoin(self.webdav_url, target_name)

        logger.info(f"Uploading {file_path} to {target_name}")
        logger.debug(f"Upload URL: {upload_url}")

        try:
            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()

            # Upload using WebDAV PUT with Basic Auth
            # Username is the share token, password is the share password
            response = requests.put(
                upload_url,
                data=file_content,
                auth=(self.share_token, self.password),
                headers={"Content-Type": "application/octet-stream"},
            )

            # Check if upload was successful
            if response.status_code in [200, 201, 204]:
                logger.info(f"Successfully uploaded {target_name}")
                return True
            else:
                logger.error(
                    f"Upload failed with status {response.status_code}: {response.text}"
                )
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Upload failed: {e}")
            raise

    def test_connection(self) -> bool:
        """Test if the connection to the share is working.

        Returns:
            True if connection is successful, False otherwise
        """
        logger.debug("Testing connection to share")

        try:
            # Try a PROPFIND request to check if we can access the share
            response = requests.request(
                "PROPFIND",
                self.webdav_url,
                auth=(self.share_token, self.password),
            )

            if response.status_code in [200, 207]:
                logger.info("Connection test successful")
                return True
            else:
                logger.warning(
                    f"Connection test failed with status {response.status_code}"
                )
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Connection test failed: {e}")
            return False
