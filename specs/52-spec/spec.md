## Objective

Add a basic `index.html` file to the project root so the repository has a minimal landing page that can be opened in a browser or served by a static file server.

## Implementation Plan

1. Create `index.html` at the repository root with standard HTML5 boilerplate.
2. Include a visible heading that identifies the project (e.g., "Test Looper") and a brief description consistent with the existing `README.md` content.
3. Ensure the file is well-formed HTML: doctype, `lang` attribute, charset, viewport meta tag.
4. Verify the file renders correctly by opening it in a browser.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `index.html` | **Create** | New file at repo root. Minimal HTML5 page with project heading and description. |
| `README.md` | No change | Already exists; no modification needed. |

## Risks

- **Trivial scope creep** — The issue says "simple"; avoid adding CSS frameworks, JavaScript, or external dependencies that inflate the deliverable.
- **Browser compatibility** — The page must render in all modern browsers; sticking to standard HTML5 avoids any issues.
- **Naming conflict** — Verify no existing `index.html` exists before creating one. The current repo has no such file, so this is safe.

## Acceptance Criteria

- `index.html` exists at the repository root.
- The file contains valid HTML5 (doctype, `html[lang]`, `head` with charset and viewport, `body`).
- The page displays a heading and short description for the project when opened in a browser.
- The file contains no broken links or references to missing resources.

Spec: specs/52-spec/spec.md
