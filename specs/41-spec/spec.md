---
issue: 41
title: "add a simple fetch.py script"
status: draft
---

## Objective

Add a simple, runnable `fetch.py` script to the project that fetches content from URLs and displays it. The script should accept a URL as a required command-line argument, support timeout and user-agent options, handle common HTTP errors gracefully, and follow minimal best practices for a Python CLI tool (shebang, error handling, clean exit codes). This script should serve as a utility for retrieving remote content programmatically.

## Implementation Plan

1. **Create `fetch.py`** at the repository root.
   - Add a `#!/usr/bin/env python3` shebang.
   - Use `urllib.request` or `requests` (if available) to fetch URL content.
   - Accept a required positional `--url` argument for the target URL.
   - Optional `--timeout` argument (default: 10 seconds) to control request timeout.
   - Optional `--user-agent` argument (default: python-requests/<version>) to set User-Agent header.
   - Print fetched content to stdout when successful.
   - Print appropriate error messages to stderr for failed requests.
   - Include an `if __name__ == "__main__"` guard.
   - Exit with code 0 on success, non-zero on failure.

2. **Make `fetch.py` executable** (`chmod +x fetch.py`).

3. **Verify** the script works correctly via:
   - `python3 fetch.py --url <test-url>` with a simple test URL
   - `./fetch.py --url <test-url>` after making it executable
   - Failed request scenarios (invalid URL, timeout, network error)

4. **Commit** the new file with a descriptive commit message referencing issue #41.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `fetch.py` | Create | New Python script that fetches content from URLs with configurable options. |

## Risks

- **No Python interpreter**: If Python 3 is not installed, the script will fail. Mitigation: document the Python 3 requirement in the script's docstring.
- **Network connectivity**: The script will fail if the target URL is unreachable. Mitigation: provide clear error messages and suggest retry options.
- **Timeout issues**: Long-running requests may hang indefinitely. Mitigation: implement timeout mechanism with user-configurable value.
- **URL validation**: Invalid URL formats may cause parsing errors. Mitigation: validate URL format before making request.
- **Output encoding**: Remote content may be in different encodings. Mitigation: handle encoding errors gracefully and provide options for output encoding.
- **SSL/TLS issues**: HTTPS certificates may be invalid or self-signed. Mitigation: provide option to disable SSL verification for testing, but warn users.

## Acceptance Criteria

- [ ] `fetch.py` exists at the repository root with a `#!/usr/bin/env python3` shebang.
- [ ] `python3 fetch.py --help` displays help message with usage instructions.
- [ ] `python3 fetch.py --url http://example.com` fetches and prints content to stdout and exits with code 0.
- [ ] `./fetch.py --url http://example.com` (after `chmod +x`) behaves identically to the `python3 fetch.py` invocation above.
- [ ] The file contains an `if __name__ == "__main__"` guard so that importing the module does not trigger the CLI path.
- [ ] The script produces output on stdout for successful requests and error messages on stderr for failures.
- [ ] No existing files are modified.
- [ ] Optional arguments `--timeout` and `--user-agent` work as specified.

---

Spec: specs/41-spec/spec.md