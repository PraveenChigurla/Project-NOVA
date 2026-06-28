# Architecture Decision Record
## NOVA-ADR-002: Python Package Restructuring

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-002 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-REPO-001 |

---

## 1. Context

The current repository layout specifies `01_Source/` as the primary directory for source code. In Python, module and package names cannot start with a digit. Attempting to import from `01_Source` directly (e.g., `import 01_Source.core`) raises a `SyntaxError: invalid decimal literal`.

We must resolve this naming restriction to ensure native compilation and autocompletion in Python development environments without resorting to run-time path manipulation hacks inside production logic.

---

## 2. Decision

We will standardize Python imports by placing the source directory itself (`01_Source`) on the Python runtime system path (`sys.path`) during development and startup, or package it for installation as a root module using a configuration file (`pyproject.toml`).

During execution:
- The top-level folder `01_Source/` remains named as specified in `NOVA-REPO-001` to maintain roadmap clarity.
- All code imports bypass the numeric folder name and import directly from the child folders:
  ```python
  from core.config_loader import ConfigurationLoader
  from shared.logger import setup_logger
  ```
- All developer testing configurations (e.g., in `pyproject.toml`) and scripts add `01_Source` to the search paths.

---

## 3. Rationale

This path-resolving decision respects the existing `01_Source` folder specification defined by the Chief Architect, while ensuring standard, compliant Python syntax across all implementation modules.

---

## 4. Consequences

### Positive
- Code files are fully compliant with native Python syntax.
- Standard IDEs (VS Code, PyCharm) can resolve package paths if developer tools are configured to recognize `01_Source` as a source root.

### Negative
- Requires a one-time path injection setup in test runners and script launchers.

---

## 5. Alternatives Considered

- **Rename folder to `nova_source/`:** Rejected to preserve strict repository structure specification alignment. Can be revisited if path injection introduces deployment overhead.
