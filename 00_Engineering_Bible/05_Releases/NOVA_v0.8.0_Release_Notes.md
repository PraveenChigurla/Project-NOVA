# Release Notes: NOVA v0.8.0

**Phase 1: Runtime Foundation** is officially complete.

## Overview
v0.8.0 marks the completion of the Project NOVA foundational architecture. The intelligence and execution pipelines have been decoupled and strictly integrated via mathematically verifiable boundaries. The system is now a general-purpose AI Execution Engine capable of routing natural language through a multi-layered security and capability framework to affect the host operating system safely.

## Key Features
*   **Kernel Core:** Centralized `NovaKernel` orchestrator managing the full subsystem lifecycle, dependency injection (`ServiceLocator`), and asynchronous message passing (`AsyncioEventBus`).
*   **Intent Framework:** Rule-based parser (`RuleIntentParser`) mapping noisy natural language inputs to strictly validated `IntentResult` schemas.
*   **Planning Framework:** Graph-based planning logic translating intents into mathematical `ExecutionPlan` Directed Acyclic Graphs (DAGs).
*   **Execution Engine:** Asynchronous pipeline that natively resolves dependencies, requests permissions, and executes capabilities using `asyncio.gather`.
*   **Execution Sub-Managers:**
    *   `ExecutionScheduler`: Resolves parallel execution layers from the Plan DAG.
    *   `RetryManager`: Applies exponential backoff using `RetryPolicy`.
    *   `RollbackManager`: Gracefully traverses backwards through execution history to reverse operations upon critical failure.
    *   `CancellationManager`: Supports safe asynchronous halting of the execution pipeline.
*   **Security & Permissions:** `PermissionManager` operating with an explicit default-deny posture. Capabilities cannot invoke Providers without explicit `PermissionScope` grants.
*   **Capability & Provider Frameworks:** Immutable runtime boundaries. Intelligence models sit inside Capabilities and push structured requests to physical OS operations managed by native Providers.
*   **Windows Desktop Provider:** The first production provider, integrating securely with Windows using zero third-party dependencies (`subprocess` and `ctypes`).

## Architectural Freeze
As of v0.8.0, the core Runtime Foundation (Capabilities, Providers, Security, Execution, Intents, Planning) is placed under a strict **Architecture Freeze**. No structural changes may be made to these frameworks without formal authorization via an Architecture Decision Record (ADR).
