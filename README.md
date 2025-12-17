# Nextcloud CLI Upload Tool

A command-line tool for uploading files to Nextcloud public share links using the WebDAV API.

## Features

- Upload files to Nextcloud public shares from the command line
- Support for password-protected shares
- Custom remote filenames
- Connection testing without uploading
- Verbose and quiet modes for logging
- Cross-platform support (macOS and Linux)
- Detailed error handling and logging

## Installation

### Prerequisites

- Python 3.8 or higher
- uv package manager (recommended) or pip

### Setup

```bash
# Clone or download this repository
cd nextcloudcli

# Create virtual environment with uv
uv venv --seed

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux

# Install the package with dependencies
uv pip install -e .

# For development with testing and linting tools
uv pip install -e ".[dev]"
```

## Usage

### Basic Command

```bash
nextcloud-upload --share-url <SHARE_URL> --file <FILE_PATH>
```

### Options

- `--share-url, -u` (required): Nextcloud public share URL
- `--file, -f` (required): Path to the file to upload
- `--password, -p`: Password for password-protected shares (optional)
- `--remote-name, -n`: Custom remote filename (optional, defaults to local filename)
- `--verbose, -v`: Enable verbose output with debug logging
- `--quiet, -q`: Suppress all output except errors
- `--test-connection, -t`: Test connection to share without uploading
- `--help`: Show help message with all options
- `--version`: Show version information

## Examples

### Upload a file to a public share

```bash
nextcloud-upload -u https://cloud.daa-pm.de/nextcloud/s/3R8KfqwSHEYCKzD -f document.pdf
```

### Upload with password-protected share

```bash
nextcloud-upload -u https://cloud.example.com/s/ShareToken -f image.jpg -p MySecretPassword
```

### Upload with custom remote filename

```bash
nextcloud-upload -u https://cloud.example.com/s/ShareToken -f local_file.txt -n remote_file.txt
```

### Test connection before uploading

```bash
nextcloud-upload -u https://cloud.example.com/s/ShareToken -f dummy.txt -t
```

### Upload with verbose logging

```bash
nextcloud-upload -u https://cloud.example.com/s/ShareToken -f file.pdf -v
```

### Upload in quiet mode (errors only)

```bash
nextcloud-upload -u https://cloud.example.com/s/ShareToken -f file.pdf -q
```

## How It Works

The tool uses the Nextcloud WebDAV API to upload files to public shares:

1. Extracts the share token from the provided share URL
2. Constructs the WebDAV endpoint URL
3. Authenticates using HTTP Basic Auth (username = share token, password = share password)
4. Uploads the file using HTTP PUT request
5. Returns success or error status

## Troubleshooting

### "Could not extract share token from URL"

Make sure your share URL is in the correct format:
- `https://cloud.example.com/s/TOKEN`
- `https://cloud.example.com/nextcloud/s/TOKEN`

### "Upload failed with status 401"

This usually means authentication failed. Check:
- Is the share URL correct?
- If the share is password-protected, did you provide the correct password with `-p`?

### "Upload failed with status 403"

The share might not allow uploads. Check the share permissions in Nextcloud.

### "File not found"

Make sure the file path you provided exists and is accessible.

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check .
```

### Type Checking

```bash
mypy src/
```

### Code Formatting

```bash
ruff format .
```

## Project Structure

```
nextcloudcli/
├── src/
│   └── nextcloudcli/
│       ├── __init__.py
│       ├── cli.py          # Command-line interface
│       └── uploader.py     # Nextcloud upload logic
├── tests/                  # Test files
├── docs/                   # Documentation
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT
