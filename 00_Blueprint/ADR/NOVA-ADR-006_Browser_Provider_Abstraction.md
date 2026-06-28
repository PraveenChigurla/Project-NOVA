# Architecture Decision Record
## NOVA-ADR-006: Replaceable Browser Provider Abstraction Layer

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-006 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CAP-BRW-008 |

---

## 1. Context

NOVA requires browser automation capability (clicking, filling forms, reading DOMs). The platform must remain decoupled from specific automation frameworks (like Playwright or Selenium) to prevent vendor lock-in, ease dependency maintenance, and support future light-weight headless browsers.

---

## 2. Decision

We will introduce an **Abstract Browser Provider Interface (`IBrowserProvider`)** in `01_Source/capabilities/browser.py`.
The core `BrowserCapability` class will interact exclusively with this interface.
Concrete automation wrappers (e.g. `PlaywrightProvider` in `01_Source/tools/playwright_wrapper.py`) will implement `IBrowserProvider`.

The interface will declare the following standard contracts:
```python
class IBrowserProvider(ABC):
    @abstractmethod
    def launch(self, browser_type: str, headless: bool, profile: Optional[str] = None) -> str: ... # Returns session ID
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def navigate(self, url: str) -> None: ...
    @abstractmethod
    def create_tab(self) -> str: ... # Returns tab ID
    @abstractmethod
    def close_tab(self, tab_id: str) -> None: ...
    @abstractmethod
    def switch_tab(self, tab_id: str) -> None: ...
    @abstractmethod
    def click_element(self, selector: str) -> None: ...
    @abstractmethod
    def fill_input(self, selector: str, text: str) -> None: ...
    @abstractmethod
    def read_dom(self) -> str: ...
    @abstractmethod
    def take_screenshot(self) -> bytes: ...
```

---

## 3. Rationale

This satisfies the "Model independence" and "Extensibility" principles of the NOVA Constitution (`NOVA-002`), ensuring that switching from Playwright to Selenium or a custom Chromium automation driver requires zero modifications to the AI Orchestration or Capability layers.

---

## 4. Consequences

### Positive
- Framework decoupling: Playwright is isolated within its wrapper.
- Simplified testing: We can write unit tests that run completely offline with a mock browser provider that returns predefined DOM strings and mock screenshots.

### Negative
- Minor translation layer overhead to map framework-specific objects (like Playwright Page instances) to generic NOVA session string references.
