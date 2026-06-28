# Project Foundation Specification
## Project NOVA Core Foundation, Governance, and Standards

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-SPEC-001 |
| **Version** | 1.0 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | None |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Consolidate Charter, Constitution, Manifesto, Onboarding, Repository Structure, Engineering Standards, and Glossary drafts. |

---

## Table of Contents
1. [Purpose & Scope](#purpose--scope)
2. [Project Charter](#project-charter)
3. [NOVA Constitution](#nova-constitution)
4. [NOVA Manifesto](#nova-manifesto)
5. [Engineer Onboarding (Antigravity Role)](#engineer-onboarding-antigravity-role)
6. [Repository Structure Specification](#repository-structure-specification)
7. [Engineering Standards](#engineering-standards)
8. [Documentation Standards](#documentation-standards)
9. [Canonical Glossary](#canonical-glossary)
10. [Foundation Roadmap](#foundation-roadmap)

---

## Purpose & Scope

This specification establishes the organizational, architectural, and operational baseline for Project NOVA. It binds all contributors—both human and AI—to unified coding, architectural, security, and procedural standards.

---

## Project Charter

### Purpose
Build NOVA as a secure, modular, and model-independent AI Operating Platform.

### Mission
Transform human intentions into safe, explainable, and intelligent execution across operating system environments.

### Roles & Responsibilities

*   **Praveen (Project Founder & Product Owner):** Sets the product vision, prioritizes milestones, runs verification tests, and provides final approvals.
*   **ChatGPT (Chief Architect):** Defines high-level platform architecture, authors technical specifications, sets security and coding standards, and conducts architectural reviews.
*   **Antigravity (Lead Software Engineering Agent):** Implements approved specifications, produces production-quality code, writes comprehensive unit tests, and conducts refactorings.

### Golden Rule
No code implementation begins until its high-level design and specific software requirements are approved by the Chief Architect.

---

## NOVA Constitution

The core principles of Project NOVA are:

1.  **Platform First:** Focus on building a reusable intelligence platform rather than a collection of ad-hoc automation scripts.
2.  **Architecture Before Implementation:** Design interfaces and write specifications before writing code.
3.  **Security by Design:** Enforce tool-level permissions, run verification checks, and capture complete audit trails.
4.  **Human Oversight:** Maintain user-in-the-loop validation barriers for destructive actions and support immediate emergency abort signals.
5.  **Explainable Behavior:** Ensure the planning logic, context state, and action steps are readable and auditable.
6.  **Modularity:** Ensure engines, services, and tools are decoupled and communicate exclusively via interfaces or event loops.
7.  **Offline-First Where Practical:** Route local automation commands to local engines to preserve privacy and function without internet access.
8.  **Model Independence:** Design provider adapters so LLM, STT, and TTS engines are swappable.
9.  **Quality Over Speed:** Prioritize clean, typed, and well-tested code over fast delivery.
10. **Long-Term Maintainability:** Think about system scaling requirements for future versions.

---

## NOVA Manifesto

Operating systems execute commands. NOVA understands intentions. 

We are building an intelligence layer that sits above the operating system to transform human intentions into safe, explainable, and intelligent execution.

---

## Engineer Onboarding (Antigravity Role)

As the Lead Software Engineering Agent:
*   **Do:** Implement approved specifications, write comprehensive test suites, keep modules decoupled, and report architectural concerns.
*   **Don't:** Rewrite core architectures without approval, bypass permission policy checks, hardcode configuration keys, or implement hidden behaviors.

---

## Repository Structure Specification

### Root Layout

Every Project NOVA repository must conform to the following directory layout:
*   `00_Blueprint/`: Engineering specifications, requirements, and Architectural Decision Records (ADRs). No code.
*   `01_Source/`: Core package source code, tests, configuration schemas, and build targets.
*   `02_Research/`: Proofs of concept, accuracy benchmarks, and evaluation notebooks.
*   `03_Experiments/`: Temporary developer playgrounds and spikes.
*   `04_Releases/`: Packaging logs and binary targets.
*   `05_Templates/`: Engineering document templates (PRS, SRS, ADR, LLD).
*   `06_Tools/`: Local developer scripts, compiler tools, and CI pipelines.

### Module Rules
*   Every module in `01_Source/` must have a corresponding test file under `tests/`.
*   Modules must communicate via clean interface classes or event streams to prevent circular imports.

---

## Engineering Standards

Every production module must comply with the following conventions:
1.  **Strong Typing:** Python type hinting is mandatory on all function signatures, variables, and returns.
2.  **Comprehensive Logging:** Emit standard events and logs indicating execution states, data inputs, and warnings.
3.  **Structured Error Handling:** Catch and handle failures gracefully. Never let unhandled thread crashes occur.
4.  **Externalized Configuration:** All configurations must live outside code modules in settings files.
5.  **Separation of Logic:** Decouple stateful reasoning (engines) from stateless workers (services).

---

## Documentation Standards

Every blueprint document must enforce the standard cover block:
*   **Document ID:** Standard format: `NOVA-TYPE-NUMBER`.
*   **Version:** Numeric versioning index.
*   **Status:** `DRAFT`, `UNDER REVIEW`, `APPROVED`, or `ACTIVE`.
*   **Dependencies:** List related specifications.
*   **Revision History Table:** Detailed summary of historical changes.

---

## Canonical Glossary

*   **Goal:** A natural-language intention provided by the user.
*   **Intention:** A structured representation of a Goal classified by intent.
*   **Plan:** An ordered sequence of Tasks compiled by the Planner.
*   **Task:** A discrete unit of work within a Plan.
*   **Action:** An atomic OS-level operation (e.g. key press, cursor click).
*   **Capability:** A reusable platform ability (e.g., Browser Control, Vision).
*   **Skill:** A user-facing grouping of capabilities (e.g., Coding Assistant).
*   **Engine:** A stateful, long-running intelligence subsystem.
*   **Service:** A stateless backend worker utility.
*   **Adapter:** An interface wrapper connecting NOVA to external system APIs.
*   **Tool:** An external utility or executable registered with the platform.
*   **Provider:** An external model or cloud service supplier.

---

## Foundation Roadmap

The project progresses through the following milestones:
1.  **Foundation Pack:** Establishes governance and index specs (Current Phase).
2.  **Product Pack:** Details target user personas and goals.
3.  **Architecture Pack:** Outlines core engines and interfaces.
4.  **AI Pack:** Establishes model providers and cognitive loops.
5.  **Capability Packs:** Details individual automation specifications.
6.  **Implementation:** Development of platform components and integration checks.
