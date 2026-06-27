# Spec: Create a simple index.html

> Issue: #52

## Objective

Add a basic `index.html` file to the repository that serves as a landing page for the project, providing a minimal but functional web page introducing the Test Looper project.

## Implementation Plan

1. Create `index.html` at the repository root with standard HTML5 boilerplate.
2. Include a page title and a brief introductory heading (e.g., project name and one-line description).
3. Optionally link to or reference the existing `greeting.py` script or `README.md` for context.
4. Verify the file renders correctly by opening it in a browser.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `index.html` | **Create** | New HTML5 file at the repo root containing a simple landing page with a heading, brief description, and basic structure. |

No existing files require modification.

## Risks

- **Scope creep**: The issue says "simple" — avoid over-engineering with frameworks, build tools, or complex layouts. Keep it as a single static HTML file.
- **Broken links**: If the page links to other files (e.g., `README.md`, `greeting.py`), ensure paths are relative and correct.
- **Encoding**: Use `UTF-8` charset to avoid rendering issues with any special characters.
- **Empty or placeholder content**: The page should have meaningful content, not just empty tags.

## Acceptance Criteria

- `index.html` exists at the repository root.
- The file is valid HTML5 (proper `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>` structure).
- The file includes a `<title>` element describing the project.
- The file contains at least one visible heading (`<h1>`) with the project name or equivalent.
- The page is viewable in any modern browser without errors.
- All existing tests and functionality (e.g., `greeting.py`) remain unaffected.

---

Spec: specs/52-spec/spec.md
