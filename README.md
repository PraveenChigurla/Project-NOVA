# Project NOVA
## Modular, Explainable, and Model-Independent AI Operating Platform

---

## Vision
Project NOVA is designed to act as a secure intelligence layer above operating systems. By transforming unstructured, natural-language human intentions into safe, explainable, and programmatically bounded workflows, NOVA bridges the gap between cognitive models and local execution environments.

---

## Engineering Philosophy
1.  **Architecture Before Implementation:** Declare boundaries, interfaces, and specifications before writing logic code.
2.  **Decoupling & Modularity:** Subsystems communicate through unified interfaces or event-driven models (`EventBus`). Direct dependency coupling is prohibited.
3.  **Model Independence:** AI cognitive planning models, speech transcribers (STT), and voice synthesizers (TTS) are wrapped behind swappable adapters.
4.  **Security by Design:** Enforce tool-level permissions validation before triggering execution emulations, maintaining strict logs and user-in-the-loop validation checkpoints.
5.  **Quality & Testability:** Ensure every core engine has matching tests to guarantee execution accuracy.

---

## Repository Layout

The repository is structured as a scalable production environment:
*   `00_Blueprint/` — Source of truth specifications, document templates, and Architectural Decision Records (ADRs).
*   `01_Source/` — Python codebase containing core engines, services, tool manager adapters, and pytest tests.
*   `02_Research/` — Technical proofs of concept, OCR accuracy studies, and benchmarks.
*   `03_Experiments/` — Safe playground folders for developer spikes.
*   `04_Releases/` — Platform deployment packages and compiled binaries.
*   `06_Tools/` — Local developer compiler scripts and pipeline configurations.
*   `99_Archive/` — Storage path for deprecated brainstorming draft packs and early working drafts.

---

## Current Milestone

We are currently at **Phase 0 — Repository Setup & Governance (Milestone 1)**. 
- All conceptual drafts have been consolidated into **8 official engineering specifications** inside `00_Blueprint/`.
- Repository directories have been refactored, and all legacy drafts have been safely archived.
- Interface structures and documentation compilers are in place.

---

## How to Navigate the Repository

*   To understand the system design: Begin by reading the **Engineering Bible** index: [00_Blueprint/README.md](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/README.md).
*   To review architecture guidelines: Read the system specification: [NOVA-SPEC-003](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/02_Architecture/NOVA-SPEC-003_System_Architecture_Specification.md).
*   To review tool decisions: Browse the [00_Blueprint/ADR/](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/00_Blueprint/ADR/) directory.
*   To build documentation: Run the local compiler script: [06_Tools/compile_docs.py](file:///c:/Users/hp/Documents/PRAVEEN/Project%20NOVA/06_Tools/compile_docs.py).
