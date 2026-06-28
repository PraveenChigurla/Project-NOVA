# Architecture Decision Record

**ID:** NOVA-ADR-008
**Title:** Phase 1 Runtime Foundation Architecture Freeze
**Date:** 2026-06-28
**Status:** Accepted

## Context
Project NOVA has completed Phase 1 (Runtime Foundation), culminating in version v0.8.0. 
The core architectures governing the Kernel, Intents, Planning, Execution Engine, Security (Permission Manager), Capabilities, and Providers have been fully implemented, integrated, and validated via end-to-end integration tests.

To ensure stability as we move into Phase 2 (which will introduce highly complex features like Local LLMs, Memory Frameworks, and Desktop UI Automation), the foundation must remain strictly immutable. Uncontrolled changes to the core execution loops or security boundaries risk introducing systemic instability.

## Decision
Effective immediately, the following namespaces are placed under an **Architecture Freeze**:

*   `nova.core.*` (Kernel, DI, Event Bus, Config)
*   `nova.execution.*` (Execution Engine, Sub-Managers, Models)
*   `nova.intelligence.planning.*` (Planners, Task Graphs)
*   `nova.intelligence.intents.*` (Parsers, Registries, Extractors)
*   `nova.security.permissions.*` (Permission Manager, Policies)
*   `nova.capabilities.base.*` and `nova.capabilities.registry.*`
*   `nova.providers.base.*` and `nova.providers.registry.*`

**No modifications to the structural design, interfaces, or architectural boundaries of these frameworks may be made without a formally drafted, reviewed, and approved Architecture Decision Record (ADR).**

## Consequences
*   **Positive:** Guarantees a stable, mathematically secure execution pipeline as we scale the intelligence capabilities of the system.
*   **Negative:** Adds slight bureaucratic overhead when genuinely useful architectural improvements to the foundation are discovered. Developers must pause and draft an ADR before refactoring the core.
