"""Command-line interface for Nextcloud file upload."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from nextcloudcli.uploader import NextcloudUploader


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging based on verbosity flags.

    Args:
        verbose: Enable debug-level logging
        quiet: Suppress all logging except errors
    """
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Configure logging format
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@click.command()
@click.option(
    "--share-url",
    "-u",
    required=True,
    help="Nextcloud public share URL (e.g., https://cloud.example.com/s/TOKEN)",
)
@click.option(
    "--file",
    "-f",
    "file_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the file to upload",
)
@click.option(
    "--password",
    "-p",
    default=None,
    help="Password for password-protected shares (optional)",
)
@click.option(
    "--remote-name",
    "-n",
    default=None,
    help="Remote filename (defaults to local filename)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output (debug logging)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all output except errors",
)
@click.option(
    "--test-connection",
    "-t",
    is_flag=True,
    help="Test connection to share without uploading",
)
@click.version_option(version="0.1.0", prog_name="nextcloud-upload")
def main(
    share_url: str,
    file_path: Path,
    password: Optional[str],
    remote_name: Optional[str],
    verbose: bool,
    quiet: bool,
    test_connection: bool,
) -> None:
    """Upload files to Nextcloud public shares via WebDAV.

    This tool allows you to upload files to Nextcloud public share links
    from the command line. It supports password-protected shares and
    custom remote filenames.

    \b
    Examples:
        # Upload a file to a public share
        nextcloud-upload -u https://cloud.example.com/s/TOKEN -f document.pdf

        # Upload with a password-protected share
        nextcloud-upload -u https://cloud.example.com/s/TOKEN -f file.txt -p secret

        # Upload with a custom remote filename
        nextcloud-upload -u https://cloud.example.com/s/TOKEN -f local.txt -n remote.txt

        # Test connection without uploading
        nextcloud-upload -u https://cloud.example.com/s/TOKEN -f dummy.txt -t
    """
    # Setup logging
    setup_logging(verbose=verbose, quiet=quiet)
    logger = logging.getLogger(__name__)

    try:
        # Initialize uploader
        logger.debug(f"Initializing uploader for share: {share_url}")
        uploader = NextcloudUploader(share_url, password)

        # Test connection if requested
        if test_connection:
            logger.info("Testing connection to share...")
            if uploader.test_connection():
                click.echo("✓ Connection successful", err=quiet)
                sys.exit(0)
            else:
                click.echo("✗ Connection failed", err=True)
                sys.exit(1)

        # Upload file
        logger.info(f"Starting upload of {file_path}")
        # Show progress bar unless in quiet mode or not in a terminal
        show_progress = not quiet and sys.stdout.isatty()
        success = uploader.upload_file(
            file_path, remote_name, show_progress=show_progress
        )

        if success:
            if not quiet:
                click.echo(f"✓ Successfully uploaded {file_path.name}")
            sys.exit(0)
        else:
            click.echo(f"✗ Failed to upload {file_path.name}", err=True)
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Invalid share URL: {e}")
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=verbose)
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
