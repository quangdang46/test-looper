# Spec: Create a simple index.html

> Issue: #52

## Objective

Add a minimal `index.html` file at the repository root to serve as a landing page for the Test Looper project. The page must be viewable in any modern browser, contain no external dependencies, and provide a brief introduction to the project alongside links to existing project files (`greeting.py`, `README.md`).

---

## Implementation Plan

### Step 1 — Determine file location

Create `index.html` in the **repository root** (`/`), co-located with the existing `greeting.py` and `README.md` files.

### Step 2 — Write the HTML file

Create `index.html` with the following structure:

| Element | Required? | Detail |
|---------|-----------|--------|
| `<!DOCTYPE html>` | Yes | HTML5 doctype |
| `<html lang="en">` | Yes | Language attribute set to English |
| `<meta charset="UTF-8">` | Yes | Inside `<head>` |
| `<meta name="viewport" content="width=device-width, initial-scale=1.0">` | Yes | Mobile-friendly rendering |
| `<title>` | Yes | Descriptive: `Test Looper` or `Test Looper Project` |
| `<h1>` | Yes | Project name (`Test Looper`) |
| `<p>` description | Yes | Brief description of the project |
| Links to `greeting.py` and `README.md` | Optional (recommended) | Relative file paths (e.g., `<a href="greeting.py">`) — recommended but not blocking |

No CSS frameworks, JavaScript, or external dependencies.

**Template structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Test Looper</title>
</head>
<body>
  <h1>Test Looper</h1>
  <p>A minimal test repository for CI/CD looping workflows.</p>
</body>
</html>
```

### Step 3 — Verify file

- Confirm the file exists at the expected path (`index.html` at repo root).
- Validate syntax is well-formed HTML5.
- Open in a browser or parse with a tool (e.g., `python -m html.parser` or `xmllint --html` if available) to confirm no unclosed tags.
- Confirm existing files (`greeting.py`, `README.md`) are untouched.

### Step 4 — Commit and push

```bash
git add index.html
git commit -m "Create simple index.html landing page (#52)"
git push origin HEAD
```

---

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `index.html` | **Create** | New file at repo root. Minimal HTML5 landing page with project heading, description, and optional links to existing files. |
| `greeting.py` | No change | Unaffected. |
| `README.md` | No change | Unaffected. |

---

## Acceptance Criteria

- [ ] `index.html` exists at the repository root.
- [ ] The file is valid HTML5 (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
- [ ] The `<head>` includes `<meta charset="UTF-8">` and a viewport meta tag.
- [ ] The `<title>` describes the project (e.g., "Test Looper").
- [ ] The `<body>` contains at least one visible heading (`<h1>`) with the project name.
- [ ] The page is viewable in any modern browser without errors.
- [ ] All existing files (`greeting.py`, `README.md`) remain unmodified and functional.

---

## Risks

| Risk | Mitigation |
|------|-------------|
| **Scope creep** — adding CSS, JS, frameworks, or complex layouts beyond "simple" | Explicit constraint: no CSS frameworks, JS, or external deps. |
| **Broken links** — if linking to `greeting.py` or `README.md`, paths must be correct | Use relative paths from repo root; verify by opening the file in a browser. |
| **Character encoding** — special characters may not render correctly | Specify `UTF-8` charset in the `<head>`. |
| **Naming conflict** — `index.html` already exists | Check with `ls index.html` before creating; repo currently has none. |
| **Existing functionality affected** — `greeting.py` must still work | The new file is static HTML — no code changes needed elsewhere. |

---

Spec: specs/52-spec/spec.md
Shell cwd was reset to /private/tmp/test-looper/.looper/worktrees/worker-a690571f-1cbc-4991-9945-1b2696fc7e4c
