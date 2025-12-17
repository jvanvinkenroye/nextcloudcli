# Contributing to Nextcloud CLI Upload Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- uv (recommended) or pip
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/jvanvinkenroye/nextcloudcli.git
cd nextcloudcli

# Create virtual environment
uv venv --seed

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install development dependencies
uv pip install -e ".[dev]"
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

Follow the code style guidelines below.

### 3. Run Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_uploader.py

# Run tests in verbose mode
pytest -v

# Run tests with specific coverage report
pytest --cov=src/nextcloudcli --cov-report=html
```

### 4. Code Quality Checks

```bash
# Run linter
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### 5. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Good commit messages:
git commit -m "feat: add batch upload functionality"
git commit -m "fix: resolve WebDAV URL construction issue"
git commit -m "docs: update README with new examples"
git commit -m "test: add tests for progress bar"

# Commit types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# test: Test changes
# refactor: Code refactoring
# chore: Maintenance tasks
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style Guidelines

### Python Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 88 characters
- Use descriptive variable names
- Add docstrings for all public functions and classes

Example:

```python
def upload_file(
    self,
    file_path: Path,
    remote_name: Optional[str] = None,
    show_progress: bool = False,
) -> bool:
    """Upload a file to the Nextcloud share.

    Args:
        file_path: Path to the local file to upload
        remote_name: Optional remote filename (defaults to local filename)
        show_progress: Show progress bar for upload (default False)

    Returns:
        True if upload was successful, False otherwise

    Raises:
        FileNotFoundError: If the local file does not exist
        requests.exceptions.RequestException: If the upload request fails
    """
    # Implementation here
```

### Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage (target: >80%)
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Use fixtures for common test data
- Mock external dependencies (HTTP requests, file system when appropriate)

Example:

```python
def test_upload_with_password_protected_share(
    sample_share_url: str,
    share_password: str,
    temp_file: Path,
    mock_successful_response,
    mocker,
) -> None:
    """Test upload to password-protected share."""
    uploader = NextcloudUploader(sample_share_url, share_password)
    mock_put = mocker.patch("requests.put", return_value=mock_successful_response)

    result = uploader.upload_file(temp_file)

    assert result is True
    assert mock_put.call_args[1]["auth"] == ("TestToken123", share_password)
```

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] No linting errors (`ruff check`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Coverage is maintained or improved
- [ ] Documentation is updated if needed
- [ ] CHANGELOG.md is updated (for significant changes)

### Pull Request Description

Include:

1. **What**: Brief description of changes
2. **Why**: Reason for the change
3. **How**: Technical approach taken
4. **Testing**: How the changes were tested
5. **Screenshots**: If applicable (for UI/CLI changes)

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Reporting Issues

### Bug Reports

Include:

- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, tool version)
- Error messages or stack traces

### Feature Requests

Include:

- Clear description of the feature
- Use case and motivation
- Proposed solution (if you have one)
- Alternatives considered

## Questions?

- Open an issue for questions
- Check existing issues and PRs first
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

Be respectful, inclusive, and professional. We aim to maintain a welcoming community for all contributors.
