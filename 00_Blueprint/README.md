# Project NOVA Engineering Bible
## Canonical Specification Directory, Governance, and Document Lifecycles

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-BIBLE-001 |
| **Version** | 1.1 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-SPEC-001 to NOVA-SPEC-009 |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Initial publication of the unified Engineering Bible. |
| 1.1 | 2026-06-28 | Antigravity | Refactored repository structure: moved capability folders, added naming conventions, directory descriptions, reading order, and indexed NOVA-SPEC-009 (AI Kernel). |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Blueprint Directory Purpose Mapping](#blueprint-directory-purpose-mapping)
3. [Specification Registry](#specification-registry)
4. [Documentation Governance Policies](#documentation-governance-policies)
5. [Document Relationships & Dependencies](#document-relationships--dependencies)
6. [Reading Order Path](#reading-order-path)
7. [Architectural Decision Records (ADRs) Index](#architectural-decision-records-adrs-index)

---

## Executive Summary

The **Engineering Bible** acts as the single source of truth and catalog index for all formal blueprints, product requirements, and system specifications in Project NOVA. It binds all development phases to structured lifecycles, naming schemas, and dependency rules.

---

## Blueprint Directory Purpose Mapping

Inside `00_Blueprint/`, files are strictly organized by engineering domains:

*   `00_Foundation/` — Core governance policies, project constitution, manifesto, onboarding rules, and repository layouts.
*   `01_Product/` — High-level product requirement documents (PRD), personas, use cases, and success metrics.
*   `02_Architecture/` — System component topologies, event structures, and Architecture Review Reports (ARR).
*   `03_Engineering/` — Coding specifications, API guidelines, styling standards, and testing criteria.
*   `04_AI/` — Cognitive planning specs, LLM wrappers, memory configurations, context states, and reflection loops.
*   `05_Capabilities/` — Reusable OS-level orchestration specs (Desktop, Browser, Vision, Voice).
*   `06_Security/` — Permission policy schemas, threat models, credential security guidelines, and safety policies.
*   `07_Operations/` — Monitoring configurations, metrics logging schemas, and operator consoles.
*   `08_Deployment/` — Packaging pipelines, build outputs, environment configs, and runtime settings.
*   `09_Roadmap/` — Project roadmaps, release milestones, and task checklists.
*   `Templates/` — Document templates for PRDs, SRDs, ADRs, and capabilities specifications.
*   `ADR/` — Formal Architecture Decision Records tracking design decisions.

---

## Specification Registry

| Document ID | Specification Name | Version | Status | Location | Dependencies |
|---|---|---|---|---|---|
| **NOVA-SPEC-001** | [Project Foundation Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/00_Foundation/NOVA-SPEC-001_Project_Foundation_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/00_Foundation/` | None |
| **NOVA-SPEC-002** | [Product Requirements Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/01_Product/NOVA-SPEC-002_Product_Requirements_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/01_Product/` | NOVA-SPEC-001 |
| **NOVA-SPEC-003** | [System Architecture Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/02_Architecture/NOVA-SPEC-003_System_Architecture_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/02_Architecture/` | NOVA-SPEC-001, NOVA-SPEC-002 |
| **NOVA-SPEC-004** | [AI Core Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/04_AI/NOVA-SPEC-004_AI_Core_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/04_AI/` | NOVA-SPEC-001 to NOVA-SPEC-003 |
| **NOVA-SPEC-005** | [Desktop Capability Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/05_Capabilities/Desktop/Desktop_Capability_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/05_Capabilities/Desktop/` | NOVA-SPEC-001 to NOVA-SPEC-003 |
| **NOVA-SPEC-006** | [Browser Capability Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/05_Capabilities/Browser/Browser_Capability_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/05_Capabilities/Browser/` | NOVA-SPEC-001 to NOVA-SPEC-003 |
| **NOVA-SPEC-007** | [Vision & OCR Capability Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/05_Capabilities/Vision/Vision_Capability_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/05_Capabilities/Vision/` | NOVA-SPEC-001 to NOVA-SPEC-003, NOVA-SPEC-005 |
| **NOVA-SPEC-008** | [Voice Capability Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/05_Capabilities/Voice/Voice_Capability_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/05_Capabilities/Voice/` | NOVA-SPEC-001 to NOVA-SPEC-004 |
| **NOVA-SPEC-009** | [NOVA Kernel Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/04_AI/NOVA-SPEC-009_NOVA_Kernel_Specification.md) | 2.0 | `APPROVED` | `00_Blueprint/04_AI/` | NOVA-SPEC-001 to NOVA-SPEC-004 |
| **NOVA-SPEC-010** | [Communication Framework Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/02_Architecture/NOVA-SPEC-010_Communication_Framework_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/02_Architecture/` | NOVA-SPEC-001 to NOVA-SPEC-003, NOVA-SPEC-009 |
| **NOVA-ERR-001** | [Engineering Review Milestone 001](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/03_Engineering/NOVA-ERR-001_Engineering_Review_Report.md) | 1.0 | `APPROVED` | `00_Blueprint/03_Engineering/` | NOVA-SPEC-001 to NOVA-SPEC-010 |
| **NOVA-ENG-002** | [Engineering Backlog](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/03_Engineering/NOVA-ENG-002_Engineering_Backlog.md) | 1.0 | `APPROVED` | `00_Blueprint/03_Engineering/` | None |
| **NOVA-ARR-002** | [Backlog Dependency Analysis](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/03_Engineering/NOVA-ARR-002_Backlog_Dependency_Analysis.md) | 1.0 | `APPROVED` | `00_Blueprint/03_Engineering/` | NOVA-ENG-002 |
| **NOVA-REP-002** | [Repository Architecture Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/03_Engineering/NOVA-REP-002_Repository_Architecture_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/03_Engineering/` | NOVA-SPEC-001 |
| **NOVA-TECH-001** | [Technology Stack Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/03_Engineering/NOVA-TECH-001_Technology_Stack_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/03_Engineering/` | NOVA-SPEC-001, NOVA-SPEC-003 |
| **NOVA-SPEC-011** | [Capability Framework Specification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/02_Architecture/NOVA-SPEC-011_Capability_Framework_Specification.md) | 1.0 | `APPROVED` | `00_Blueprint/02_Architecture/` | NOVA-SPEC-003, NOVA-SPEC-009 |

---

## Documentation Governance Policies

### 1. Naming Conventions
All files created in the Blueprint directory must follow these naming patterns:
*   **Specifications:** `NOVA-SPEC-###_Specification_Name.md`
*   **Engineering Standards:** `NOVA-ENG-###_Standard_Name.md`
*   **Architecture Review Reports:** `NOVA-ARR-###_Report_Name.md`
*   **Engineering Review Reports:** `NOVA-ERR-###_Report_Name.md`
*   **Architectural Decision Records:** `NOVA-ADR-###_Decision_Name.md`

### 2. Versioning Policy
*   Draft documents must be tagged as version `0.x` with status `DRAFT`.
*   Once reviewed by the Chief Architect and Project Founder, files increment to version `1.0` and status changes to `APPROVED`.
*   Major architectural or API schema shifts increment the major version number (`2.0`, `3.0`), requiring a corresponding Architecture Decision Record (ADR) reference.
*   Minor description clarifications increment the minor version number (`1.1`, `1.2`).

---

## Document Relationships & Dependencies

Specifications maintain a cascading dependency chain:

```
[SPEC-001: Foundation]
       ↓
[SPEC-002: Product Requirements]
       ↓
[SPEC-003: System Architecture]
    ├── [SPEC-010: Communication Framework]
    ├── [SPEC-004: AI Core]
    │      ├── [SPEC-009: NOVA Kernel]
    │      │      └── [SPEC-008: Voice Capability]
    │      └── [SPEC-008: Voice Capability]
    └── [SPEC-005: Desktop Capability]
           ├── [SPEC-006: Browser Capability]
           └── [SPEC-007: Vision & OCR Capability]
```

---

## Reading Order Path

Contributors must review the blueprints in this path sequence:
1.  **NOVA-SPEC-001 (Foundation):** Introduces organizational principles, coding guidelines, and repository layouts.
2.  **NOVA-SPEC-002 (Product):** Defines personas, functional criteria, and initial product use cases.
3.  **NOVA-SPEC-003 (Architecture):** Explains Component layering and interface communications.
4.  **NOVA-SPEC-004 (AI Core) & NOVA-SPEC-009 (NOVA Kernel):** Defines cognitive planning loops, memory indices, and central kernel orchestration.
5.  **NOVA-SPEC-005 & NOVA-SPEC-008 (Capabilities):** Explains low-level OS automation APIs (Desktop, Browser, Vision, Voice).

---

## Architectural Decision Records (ADRs) Index

All active architecture decisions are documented under the [00_Blueprint/ADR/](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/) directory:
*   [NOVA-ADR-002: Python Package Restructuring](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-002_Python_Package_Restructuring.md)
*   [NOVA-ADR-003: Decoupled Subsystem Event-Driven Communication](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-003_Decoupled_EventBus_Interface.md)
*   [NOVA-ADR-004: Tool-Level Permission Verification](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-004_Permission_Policy_Enforcer.md)
*   [NOVA-ADR-005: AI Provider Abstraction Separation](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-005_AI_Provider_Separation.md)
*   [NOVA-ADR-006: Replaceable Browser Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-006_Browser_Provider_Abstraction.md)
*   [NOVA-ADR-007: Vision and OCR Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-007_Vision_OCR_Provider_Abstraction.md)
*   [NOVA-ADR-008: Voice STT and TTS Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-008_Voice_STT_TTS_Provider_Abstraction.md)
