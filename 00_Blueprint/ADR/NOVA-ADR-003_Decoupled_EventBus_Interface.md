# Architecture Decision Record
## NOVA-ADR-003: Decoupled Subsystem Event-Driven Communication

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-003 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CMP-001 |

---

## 1. Context

NOVA is a modular AI Operating Platform. As the system scales to support more capabilities and plugins, direct coupling between engines (e.g. `PlannerEngine` importing and calling `MemoryEngine` directly) will lead to circular dependency locks, testing difficulties, and brittle architectures.

---

## 2. Decision

All stateful engines (e.g. Planner, Voice, Vision, Memory) must communicate exclusively by emitting and subscribing to events on a global `EventBus` implemented under `01_Source/core/`. Direct instantiation or direct calls of other engines' APIs are prohibited.

---

## 3. Rationale

This enforces the constitutional principle of Modularity (`NOVA-002`). By decoupled event passing, engines can be loaded, unloaded, mocked, or rewritten independently.

---

## 4. Consequences

### Positive
- Strict isolation of engine lifecycles.
- Simplified unit testing (each engine can be tested by asserting event sequences without loading other engines).
- Model-agnostic integrations (additional agents can listen to the event stream without changing core logic).

### Negative
- Traceability can be more complex compared to standard synchronous function calls. This will be mitigated by enforcing trace ID headers on all emitted events.
