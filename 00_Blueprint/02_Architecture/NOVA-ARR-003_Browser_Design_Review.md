# Browser Capability Design Review
## Evaluation of Browser Automation Capability Pack (NOVA-CAP-BRW v1.0)

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ARR-003 |
| **Version** | 1.0 |
| **Status** | `UNDER REVIEW` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CAP-BRW-001 to NOVA-CAP-BRW-008 |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Initial release. Completed design review of the Browser Automation specs and provider interfaces. |

---

## 1. Executive Summary

This design review evaluates the Browser Automation Capability specifications (`NOVA_Capability_Pack_5B_Browser_v1.0`). We analyze completeness, propose an implementation roadmap, and design standard interfaces to prevent framework vendor lock-in, ensuring compliance with our modular architecture principles.

---

## 2. Completeness & Consistency Review

The capability specifications are consistent and map clearly to functional requirements:
*   **Web Observation:** The separation of screen observation (acquiring visual frames and DOM trees) from visual parsing (OCR, which is handled in the `VisionEngine` / `OCRService`) is correct and avoids component bloat.
*   **Missing Specifications:** We identified a gap in session persistence and credential injection. To "restore sessions" (`NOVA-CAP-BRW-002`), the system needs access to cookies, localStorage, and browser profiles. Standard storage directories must be explicitly path-configured to prevent profile lock conflicts during concurrent executions.

---

## 3. Replaceable Provider Abstraction Design

Per **NOVA-ADR-006**, we decouple the capability API from specific automation drivers by introducing the `IBrowserProvider` interface:

*   **Boundary:** The core `BrowserCapability` (registered with `ToolManager`) handles high-level commands, validates URLs, and formats observation outputs.
*   **Decoupling:** Framework-specific scripts (e.g. Playwright selectors, Selenium execution logic) are encapsulated entirely inside wrapper classes implementing `IBrowserProvider`.
*   **Interchangeability:** If we switch from Playwright to Selenium, the `BrowserCapability` code remains completely untouched. Only the active provider instance is swapped in the configuration.

---

## 4. Security & Safety Considerations

To satisfy "Security by Design" (`NOVA-002`), browser execution must enforce:
1.  **Sensitive Domain Barriers:** A configurable URL blacklist/whitelist (e.g., blocking automated access to banking domains, payment gateways, and credential managers by default unless marked for explicit confirmation).
2.  **Secret Redaction in Logs:** Any form filling action (`type_text`) targeting inputs with type `password` or matching credentials labels must redact the values in the Audit Log to prevent security leaks.
3.  **Local File Verification:** Before executing file uploads (`NOVA-CAP-BRW-004`), the target file path must be verified against the local `PermissionPolicy` rules to prevent exfiltration of system files.

---

## 5. Proposed Implementation Roadmap

We propose a four-milestone roadmap for implementation:

*   **Milestone 1 (Interface and Setup):** Define `IBrowserProvider` and `BrowserCapability` boundaries in `01_Source/capabilities/browser.py`.
*   **Milestone 2 (Playwright Wrapper Implementation):** Build the concrete `PlaywrightProvider` in `01_Source/tools/playwright_wrapper.py` supporting browser launching, navigation, and basic page clicks.
*   **Milestone 3 (Observation Integration):** Implement DOM acquisition and structured page summaries to supply to the Vision Engine.
*   **Milestone 4 (Security Policies & Tests):** Build cross-browser testing suites and coordinate permission checks within the Tool Manager.

*Implementation is paused waiting for approval.*
