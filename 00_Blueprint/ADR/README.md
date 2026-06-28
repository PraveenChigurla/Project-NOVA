# Architectural Decision Records (ADRs)

This directory hosts all formal Architectural Decision Records (ADRs) for Project NOVA.

## Index of Decisions

- [NOVA-ADR-002: Python Package Restructuring](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/NOVA-ADR-002_Python_Package_Restructuring.md) — Outlines strategies to bypass numerical folder name restrictions for python imports.
- [NOVA-ADR-003: Decoupled Subsystem Event-Driven Communication](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-003_Decoupled_Subsystem_Event_Driven_Communication.md) — Enforces EventBus communication between stateful engines.
- [NOVA-ADR-004: Tool-Level Permission Verification](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-004_Permission_Policy_Enforcer.md) — Establishes permission enforcement within the Tool Manager.
- [NOVA-ADR-005: AI Provider Abstraction Separation from System Tools](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-005_AI_Provider_Separation.md) — Isolates AI cognitive reasoning interfaces from execution tool structures.
- [NOVA-ADR-006: Replaceable Browser Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-006_Browser_Provider_Abstraction.md) — Implements IBrowserProvider interface to isolate automation frameworks like Playwright.
- [NOVA-ADR-007: Vision and OCR Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-007_Vision_OCR_Provider_Abstraction.md) — Implements IOCRProvider and IVisionModelProvider interfaces to isolate vision and text-extraction dependencies.
- [NOVA-ADR-008: Voice STT and TTS Provider Abstraction Layer](file:///c:/Users/hp/Documents/PRAVEEN%20NOVA/00_Blueprint/ADR/NOVA-ADR-008_Voice_STT_TTS_Provider_Abstraction.md) — Implements ISTTProvider and ITTSProvider interfaces to isolate audio processing and voice generation dependencies.

---

## What is an ADR?

An Architectural Decision Record (ADR) is a document that captures an important architectural decision, including its context, alternatives considered, chosen path, rationale, and consequences.

## Structure of an ADR

Every ADR must follow the standard layout defined in `05_Templates/ADR_Template.md`:

1. **Title:** Unique ID and descriptive title (e.g., `NOVA-ADR-001: Language Selection`)
2. **Status:** `DRAFT`, `UNDER REVIEW`, `APPROVED`, `SUPERSEDED`, or `REJECTED`
3. **Context:** What is the problem we are solving? What forces are at play?
4. **Decision:** What is the chosen path?
5. **Consequences:** What is the impact? What do we gain or lose?
6. **Alternatives Considered:** What other options were investigated? Why were they rejected?
