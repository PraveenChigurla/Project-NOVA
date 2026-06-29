# NOVA-STD-801: Platform Governance
**Status:** DRAFT / PROPOSED

This document defines the rules for evolving the Project NOVA standard and ecosystem over time without fracturing compatibility or violating the core Constitution.

## 1. Versioning
Project NOVA adheres strictly to Semantic Versioning (`MAJOR.MINOR.PATCH`). 
However, versioning applies to the **Standard Contracts**, not just the implementation code.

* **MAJOR (e.g., v2.0)**: Incompatible contract changes (e.g., changing the schema of `GoalContract`, removing a mandatory Capability). 
* **MINOR (e.g., v1.1)**: Backwards-compatible additions (e.g., adding a new optional property to `ExecutionPlan`, defining a new standardized Capability).
* **PATCH (e.g., v1.0.1)**: Bug fixes in documentation, clarifications, or non-breaking implementation fixes in reference clients.

## 2. Deprecation Policy
No feature, contract, or capability defined in a `MAJOR` version may be removed until the next `MAJOR` version.
If a feature is deprecated in `v1.2`, it must remain fully functional and supported for the entirety of the `v1.x` lifecycle. It will emit a `DeprecationWarning` in the Event Chronicle, but it will not break deterministic execution.

## 3. Migration Rules
When a `MAJOR` version is released, the reference implementation MUST provide a deterministic migration path for:
*   `.nova` Packages
*   `.kpkg` Knowledge Packages
*   Sovereign Memory Databases

If a user's local intelligence cannot be migrated deterministically, the `MAJOR` version release is blocked.

## 4. Extension Approval
To maintain the safety of the Cognitive Federation, all public `.nova` packages and `.kpkg` knowledge packages submitted to the global marketplace must pass automated Governance checks:
1.  **SBOM Completeness**: Dependencies must be fully mapped.
2.  **Capability Sandboxing**: Extensions cannot request undocumented capabilities.
3.  **Trust Validation**: The publisher signature must be valid.

## 5. The Standard Evolution Process (RFC)
To propose a change to the Project NOVA Standard, developers must submit a Request for Comment (RFC).
An RFC must prove that the proposed change:
1.  Does not violate the Five Laws of NOVA Intelligence.
2.  Is necessary to solve a problem that cannot be solved via a third-party `.nova` extension.
3.  Maintains deterministic execution.

No new architectural primitives shall be introduced after Version 1.0 unless they proceed through this Governance process.
