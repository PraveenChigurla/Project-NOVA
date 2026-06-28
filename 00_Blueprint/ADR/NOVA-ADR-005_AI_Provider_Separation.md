# Architecture Decision Record
## NOVA-ADR-005: AI Provider Abstraction Separation from System Tools

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-005 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CMP-001, NOVA-TOOL-001 |

---

## 1. Context

In `NOVA-TOOL-001_Tool_Manager.md`, "LLM Providers" are listed as examples of tools managed by the Tool Manager. However, LLM reasoning is a core capability consumed directly by the `PlannerEngine`, `ReflectionEngine`, and the `AIKernel` for cognitive processing. 

If LLM access is routed through the standard `ToolManager` (which itself is invoked by execution blocks), it creates a circular dependency logic flow: the Planner uses the Tool Manager to call the LLM to write the Plan, but the Tool Manager requires the Plan to execute LLM calls.

---

## 2. Decision

We will separate AI/LLM model providers from standard execution tools:
- Standard tools (Browser Control, Git, Docker) are managed by the `ToolManager` and subject to permissions.
- LLM model providers are accessed via a dedicated **AI Provider Abstraction Layer (`IAIProvider`)** directly accessible by the AI Kernel, Planner, and Reflection subsystems.
- Model adapters (OpenAI, Anthropic, local model wrappers) will implement the `IAIProvider` interface.

---

## 3. Rationale

This prevents circular dependency loops between the `PlannerEngine` and the `ToolManager` and simplifies LLM context/token tracking.

---

## 4. Consequences

### Positive
- Clear separation between cognitive reasoning (Planner/Kernel LLM calls) and task execution (standard tools).
- Simplifies permission policies: standard tools require user permission checks, while core cognitive LLM calls do not pass through the execution check barrier (as they do not alter the filesystem/OS).

### Negative
- Developers must maintain two separate plugin patterns (Model Providers vs. Standard Tools). This is mitigated by clear template differentiation.
