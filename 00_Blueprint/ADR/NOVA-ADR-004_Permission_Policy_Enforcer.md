# Architecture Decision Record
## NOVA-ADR-004: Tool-Level Permission Verification

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-004 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CMP-001 |

---

## 1. Context

NOVA automates system interaction. Executing commands or modifying files presents security risks. We must guarantee that all executable operations pass through permission policy gates before execution.

---

## 2. Decision

The `ToolManager` is the single point of entry for all executable tools. The `ToolManager` must check permission grants with the `PermissionEngine` before delegating any action to wrappers or adapters. No tool execution can bypass this gate.

---

## 3. Rationale

This satisfies the "Security by design" constitutional principle. Isolating checks inside the `ToolManager` prevents individual engines from forgetting to check permissions.

---

## 4. Consequences

### Positive
- Centralized auditing and security compliance.
- Simplifies tool developers' work: they only need to declare required permissions rather than write check logic.

### Negative
- Minor performance overhead on tool invocation (negligible compared to LLM latency).
