# Spec: Issue #41 - add a simple fetch.py script

## Objective
Create a Python script called `fetch.py` that performs an HTTP GET request to https://example.com and prints the HTTP status code from the response. This script demonstrates basic web fetching functionality in Python using standard libraries.

## Implementation Plan
1. Create the `specs/41-spec/` directory structure if it doesn't exist
2. Create `fetch.py` at the repository root (or in an appropriate scripts directory)
3. Implement HTTP GET request using `urllib.request` or `requests` library
4. Extract and print the HTTP status code from the response
5. Add error handling for network issues and HTTP errors
6. Make the script executable with a shebang line
7. Add minimal documentation/comments
8. Test the script manually to verify functionality
9. Ensure the script follows Python best practices and PEP8 guidelines

## Files to Change
- **New file created**: `fetch.py`
  - Contains Python script to fetch URL and print HTTP status code
  - Includes proper error handling and informative output
  - Follows Python best practices and PEP8 style guidelines
  - Includes shebang for Linux/Unix execution

## Risks
- **Network dependencies**: The script requires internet connectivity to fetch https://example.com, which may not be available in all environments
- **External service availability**: The example.com service could be temporarily unavailable or return non-200 status codes
- **Python version compatibility**: Different Python versions may have varying behavior with HTTP libraries
- **Rate limiting**: While example.com is unlikely to rate-limit, the script should handle potential rate limiting gracefully
- **SSL/TLS issues**: HTTPS certificate validation could cause issues in some environments

## Acceptance Criteria
- [ ] The script can successfully fetch https://example.com and print a valid HTTP status code (e.g., "Status code: 200")
- [ ] The script handles network errors gracefully and provides meaningful error messages
- [ ] The script follows PEP8 style guidelines and includes appropriate comments
- [ ] The script includes a shebang line and is executable (`#!/usr/bin/env python3`)
- [ ] The script includes basic error handling for HTTP errors, network issues, and timeouts
- [ ] The script provides clear, user-friendly output showing the status code or error
- [ ] All existing tests continue to pass
- [ ] The new script follows the project's coding standards and conventions

Spec: specs/41-spec/spec.md