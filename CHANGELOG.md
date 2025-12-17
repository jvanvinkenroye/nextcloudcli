# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Progress bar for file uploads using tqdm
- Comprehensive test suite with 94% code coverage
- Detailed documentation (LICENSE, CHANGELOG, CONTRIBUTING)

## [0.1.0] - 2025-12-18

### Added
- Initial release of nextcloudcli
- CLI tool for uploading files to Nextcloud public shares via WebDAV
- Support for password-protected shares
- Connection testing feature (`--test-connection`)
- Verbose and quiet logging modes
- Custom remote filename support
- Streaming file upload with progress tracking
- Comprehensive test suite with pytest
  - 45 unit and integration tests
  - 88.65% code coverage
  - Mock-based testing for HTTP requests
- Type hints throughout codebase
- Support for Python 3.9+

### Features
- Upload files to Nextcloud public share links
- Password protection support for shares
- Progress bar for uploads (automatically enabled in terminals)
- Verbose (`-v`) and quiet (`-q`) modes
- Test connection before uploading (`-t`)
- Custom remote filenames (`--remote-name`)
- Short option flags (`-u`, `-f`, `-p`, `-n`, `-v`, `-q`, `-t`)

### Technical
- WebDAV-based file upload
- HTTP Basic Authentication with share token
- Streaming uploads for memory efficiency
- Comprehensive error handling and logging
- Cross-platform support (macOS, Linux)

[Unreleased]: https://github.com/jvanvinkenroye/nextcloudcli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jvanvinkenroye/nextcloudcli/releases/tag/v0.1.0
