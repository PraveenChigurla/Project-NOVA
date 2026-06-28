# NOVA Glossary
## The Official Vocabulary of Project NOVA

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-GLOSS-001 |
| **Version** | 1.0 |
| **Status** | ✅ Approved |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-ONBOARD-001 |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Initial release. Full glossary drafted from onboarding document and architectural intent. |

---

## Purpose

This document defines the official vocabulary of Project NOVA.

Every term defined here is **canonical**. When any member of the NOVA team — human or AI — uses a term listed in this glossary, they are referring to its definition as stated here, and no other interpretation.

This glossary exists because **language precision is architecture**.

Ambiguous terminology leads to:
- Misaligned implementations
- Incorrect integrations
- Wasted engineering effort
- Untestable specifications

This document prevents all of the above.

---

## Scope

This glossary applies to:
- All product discussions
- All architecture documents
- All engineering specifications
- All code, comments, and documentation
- All communications between team members (human and AI)

---

## How to Use This Document

- When writing any NOVA document, use only terms defined here.
- If a concept requires a new term, propose it via an ADR (Architecture Decision Record) before using it.
- If a term here conflicts with common usage, the NOVA definition takes precedence within project scope.
- Terms are listed alphabetically within each category.

---

## Term Categories

1. [Platform Concepts](#1-platform-concepts)
2. [Structural Units](#2-structural-units)
3. [Execution Layer](#3-execution-layer)
4. [Intelligence Layer](#4-intelligence-layer)
5. [Integration Layer](#5-integration-layer)
6. [Data & Memory](#6-data--memory)
7. [Configuration & Policy](#7-configuration--policy)
8. [Observability](#8-observability)
9. [Development & Process](#9-development--process)
10. [Document Types](#10-document-types)
11. [Roles](#11-roles)
12. [Status Terms](#12-status-terms)

---

## 1. Platform Concepts

These terms describe NOVA's identity and top-level model.

---

### AI Operating Platform

**What it is:**
NOVA's fundamental classification. An AI Operating Platform is a software system that accepts human intentions and translates them into safe, explainable, and intelligent execution across operating system environments.

**What it is not:**
- A voice assistant
- A chatbot
- A desktop automation script
- A browser automation framework

**Usage:**
> "NOVA is an AI Operating Platform. It sits above the OS and transforms goals into execution."

---

### Capability

**What it is:**
A major, named platform ability that NOVA can offer to users or to other internal components. Capabilities represent *what NOVA can do* at a high level. They are declarative — they describe an ability, they do not perform execution themselves.

**Key property:**
Capabilities do not perform work directly. They expose interfaces through which work can be requested.

**Examples:**
- `Voice` — the ability to receive and produce spoken language
- `Vision` — the ability to perceive and interpret screen content
- `Memory` — the ability to store and retrieve context over time
- `Automation` — the ability to perform sequences of system actions
- `Planning` — the ability to decompose goals into executable steps
- `Browser Control` — the ability to navigate and interact with web browsers

**What it is not:**
A Capability is not an Engine, Service, or Tool. It is the *interface contract* that those components fulfill.

**Usage:**
> "The Vision Capability is fulfilled by the Vision Engine and the OCR Service."

---

### Goal

**What it is:**
A human-expressed intention that NOVA receives as its primary input. Goals are unstructured, ambiguous, and natural. NOVA's Planner decomposes Goals into Plans.

**Examples:**
- "I want to continue my machine learning project."
- "Research the latest papers on transformers."
- "Prepare a summary of yesterday's meeting."

**What it is not:**
A Goal is not a Command, Instruction, or Action. It does not specify *how* something should be done.

**Usage:**
> "The user expressed a Goal. The Planner will decompose it into a Plan."

---

### Intention

**What it is:**
The structured interpretation of a user's Goal, produced by the Intent Detection subsystem. An Intention captures what the user wants to achieve, stripped of ambiguity.

**Usage:**
> "After processing the Goal, the Intent Detection module produced an Intention with type `RESTORE_WORKSPACE`."

---

### Platform

**What it is:**
The totality of NOVA — all Engines, Services, Capabilities, Tools, Adapters, Plugins, and configuration that constitute the running system.

**Usage:**
> "The Platform shall support multiple concurrent Sessions."

---

### Session

**What it is:**
A single, bounded interaction between a user and NOVA. A Session begins when the user initiates contact and ends when the interaction concludes. Sessions have state, history, and a lifecycle.

**Usage:**
> "Each Session has its own Memory context that is persisted at Session end."

---

## 2. Structural Units

These terms describe how NOVA is organized internally.

---

### Engine

**What it is:**
A major named subsystem of NOVA responsible for a specific domain of intelligence or execution. Engines are long-running, stateful, and typically expose an internal API consumed by other Engines or Services.

**Naming convention:**
All Engines follow the format: `[Domain] Engine`

**Examples:**
- `Planner Engine` — decomposes Goals into Plans
- `Vision Engine` — processes visual input from the screen
- `Voice Engine` — handles speech recognition and synthesis
- `Memory Engine` — manages short-term and long-term context

**What it is not:**
An Engine is not a Service (which is stateless) or a Tool (which is external and executable).

**Usage:**
> "The Planner Engine receives an Intention and produces a Plan."

---

### Module

**What it is:**
A self-contained, independently testable unit of code within an Engine or Service. A Module encapsulates a specific responsibility and exposes a well-defined interface.

**Key property:**
Modules do not depend on each other directly. They communicate through interfaces or events.

**Examples:**
- `Intent Classifier Module` within the Planner Engine
- `Frame Capture Module` within the Vision Engine

**What it is not:**
A Module is not a Python module (file), a Plugin, or an Engine. This is a NOVA architectural unit.

**Usage:**
> "The Intent Classifier Module is responsible for mapping raw Intentions to canonical Intent Types."

---

### Service

**What it is:**
A backend component that provides a specific, well-scoped function to the Platform. Services are typically stateless (or manage their own isolated state), expose a defined API, and can be replaced or upgraded independently.

**Naming convention:**
All Services follow the format: `[Domain] Service`

**Examples:**
- `OCR Service` — extracts text from screen regions
- `Memory Service` — reads and writes to the memory store
- `Settings Service` — manages configuration values
- `Permission Service` — evaluates and enforces permission policies

**What it is not:**
A Service is not an Engine (which is stateful and complex) or a Tool (which is an external executable component).

**Usage:**
> "The OCR Service exposes a `extract_text(region)` interface consumed by the Vision Engine."

---

### Plugin

**What it is:**
An externally developed or optionally installed extension to NOVA that adds new Capabilities, Skills, or Tool integrations without modifying core Platform code. Plugins follow a defined Plugin Interface contract.

**Key property:**
The Platform runs without any Plugin installed. Plugins extend — they do not replace.

**Examples:**
- `GitHub Plugin` — adds Git-aware Capabilities
- `Notion Plugin` — integrates with the Notion workspace
- `Spotify Plugin` — adds music control Capabilities

**What it is not:**
A Plugin is not a core Service, Engine, or Adapter. It is an optional extension point.

**Usage:**
> "The GitHub Plugin registers the `git_commit` and `git_push` Tools with the Tool Manager."

---

### Skill

**What it is:**
A named, user-facing combination of Capabilities that NOVA exposes as a coherent feature. Skills represent what the user experiences, composed from underlying Capabilities.

**Examples:**
- `Coding Assistant` — uses Voice, Memory, Planner, Terminal, Files, Git Capabilities
- `Research Assistant` — uses Browser Control, Memory, Vision, Planning Capabilities
- `Meeting Summarizer` — uses Voice, Memory, File Capabilities

**What it is not:**
A Skill is not a single Capability or a Tool. It is a curated composition of multiple Capabilities.

**Usage:**
> "When the user activates the Coding Assistant Skill, NOVA initializes the required Capabilities."

---

## 3. Execution Layer

These terms describe how NOVA performs work.

---

### Action

**What it is:**
The lowest-level executable operation in NOVA. An Action is atomic — it performs exactly one thing and produces a result. Actions are the primitives from which all higher-level behavior is composed.

**Examples:**
- `Click(x, y)` — clicks a screen coordinate
- `Scroll(direction, amount)` — scrolls a UI element
- `Open(path)` — opens a file or application
- `Press(key)` — sends a keyboard input
- `Copy()` — copies selected content to clipboard
- `Paste()` — pastes clipboard content
- `Move(x, y)` — moves cursor to a coordinate
- `Type(text)` — types a string of text

**Key property:**
Actions are observable, loggable, and undoable where the OS permits.

**What it is not:**
An Action is not a Workflow, Plan, or Task. It is the final step of decomposition before OS interaction.

**Usage:**
> "The Automation Engine executed three Actions: `Open`, `Type`, `Press`."

---

### Plan

**What it is:**
A structured sequence of Tasks produced by the Planner Engine from an Intention. A Plan has explicit steps, dependencies, expected outcomes, and a rollback strategy.

**Usage:**
> "The Planner Engine produced a Plan with five Tasks to fulfill the user's Goal."

---

### Task

**What it is:**
A discrete unit of work within a Plan. A Task is assigned to a specific Engine, Service, or Tool. Tasks are ordered, trackable, and produce observable outputs.

**Examples:**
- `Open VS Code`
- `Navigate to project directory`
- `Run development server`

**What it is not:**
A Task is not an Action (too granular) or a Plan (too broad). It is a mid-level work unit.

**Usage:**
> "The Plan contained a Task assigned to the Automation Engine: `Open VS Code`."

---

### Workflow

**What it is:**
A user-defined or NOVA-suggested named sequence of Tasks that the user wishes to execute repeatedly or on trigger. Workflows are saved, named, and reusable.

**Examples:**
- `Morning Routine` — opens apps, checks calendar, loads browser tabs
- `End of Day` — saves files, commits code, locks screen
- `Research Session` — opens browser, creates notes file, sets focus mode

**Key property:**
Workflows are persistent. They survive Session boundaries and can be triggered by name, schedule, or context.

**What it is not:**
A Workflow is not a one-time Plan. It is a saved, reusable pattern.

**Usage:**
> "The user triggered the `Morning Routine` Workflow. NOVA executed its Tasks."

---

### Tool

**What it is:**
An external, executable component that NOVA invokes to perform a specific technical function. Tools are concrete implementations — they touch the real world (filesystem, network, screen, process).

**Examples:**
- `Playwright` — browser automation
- `Whisper` — speech-to-text
- `Tesseract / EasyOCR` — optical character recognition
- `Git` — version control operations
- `Docker` — container management
- `FFmpeg` — audio/video processing

**Key property:**
Tools are invoked, not owned. NOVA calls Tools through the Tool Manager. Tools can be swapped for alternatives without changing Platform logic.

**What it is not:**
A Tool is not an Action, Service, or Engine. It is an external capability the Platform uses.

**Usage:**
> "The Vision Engine invoked the `EasyOCR` Tool via the Tool Manager to extract text."

---

### Tool Manager

**What it is:**
The central NOVA component responsible for registering, resolving, invoking, and monitoring Tools. The Tool Manager enforces permission checks before any Tool execution.

**Usage:**
> "All Tool invocations must pass through the Tool Manager. Direct Tool calls are prohibited."

---

## 4. Intelligence Layer

These terms describe NOVA's AI and reasoning components.

---

### Model

**What it is:**
An AI foundation model used by NOVA for reasoning, language understanding, generation, or other cognitive tasks. Models are provided by external Providers.

**Examples:**
- GPT-4o (OpenAI)
- Claude Sonnet (Anthropic)
- Qwen (Alibaba)
- Gemini (Google)

**Key property:**
Models are swappable. NOVA does not depend on any single Model. The Provider Abstraction Layer handles model-specific differences.

**Usage:**
> "The Planner Engine uses the configured Model to decompose the Intention into a Plan."

---

### Provider

**What it is:**
An organization or system that supplies a Model or external AI/data service to NOVA. Providers are accessed through Adapters.

**Examples:**
- `OpenAI` — provides GPT-series models
- `Anthropic` — provides Claude-series models
- `Google DeepMind` — provides Gemini models
- `Whisper` — provides speech recognition

**Key property:**
NOVA never calls a Provider directly from business logic. All Provider access goes through an Adapter.

**Usage:**
> "The current Provider is OpenAI. Switching to Anthropic requires only an Adapter configuration change."

---

### Intent Detection

**What it is:**
The process by which NOVA interprets a raw user Goal and produces a structured Intention. Intent Detection may involve NLP, ML classification, or LLM-based reasoning.

**Usage:**
> "Intent Detection classified the user's Goal as a `RESTORE_WORKSPACE` Intention."

---

### Reflection

**What it is:**
NOVA's post-execution self-evaluation process. After a Plan executes, the Reflection process evaluates whether the outcome matched the Goal, identifies errors, and updates Memory accordingly.

**Usage:**
> "After execution, the Reflection process determined that the Goal was only 80% fulfilled and logged a follow-up Task."

---

### Observation

**What it is:**
The process by which NOVA monitors the environment during and after execution to verify that Actions and Tasks are producing expected outcomes. Observation feeds data back into the Reflection process.

**Usage:**
> "The Observation component detected that the expected window did not open. The Plan was paused."

---

## 5. Integration Layer

These terms describe how NOVA interfaces with the outside world.

---

### Adapter

**What it is:**
A component that translates between NOVA's internal interfaces and external systems, platforms, or APIs. Every external dependency is accessed through an Adapter.

**Naming convention:**
All Adapters follow the format: `[Target] Adapter`

**Examples:**
- `Windows Adapter` — translates NOVA Actions to Windows API calls
- `Linux Adapter` — translates NOVA Actions to Linux system calls
- `Playwright Adapter` — wraps Playwright's API for NOVA Tool invocations
- `OpenAI Adapter` — translates NOVA Model requests to OpenAI API calls

**Key property:**
Adapters are the only place in the Platform where external API details exist. Business logic is never aware of which Adapter is active.

**Usage:**
> "The Automation Engine calls the `Windows Adapter` to perform screen interactions."

---

### Environment

**What it is:**
The context in which NOVA operates or within which Actions are executed. An Environment defines the application space and interaction rules.

**Examples:**
- `Desktop` — the Windows/macOS/Linux desktop shell
- `Browser` — a running web browser instance
- `Terminal` — a command-line shell session
- `VS Code` — the VS Code editor environment
- `Docker` — a running container environment
- `Excel` — the Microsoft Excel spreadsheet environment

**Key property:**
NOVA may operate across multiple Environments simultaneously. Each Environment has its own Adapter.

**Usage:**
> "The Task requires switching from the Desktop Environment to the Browser Environment."

---

## 6. Data & Memory

These terms describe NOVA's data architecture.

---

### Memory

**What it is:**
NOVA's persistent and ephemeral context storage system. Memory allows NOVA to maintain continuity across Sessions, recall user preferences, and learn from past interactions.

**Types:**
- `Short-Term Memory` — context within a single Session. Discarded at Session end unless promoted.
- `Long-Term Memory` — context persisted across Sessions. Stored in the Memory Service.
- `Working Memory` — the active context window available to the Planner Engine during Plan execution.

**Usage:**
> "The Memory Engine promoted the user's project context from Short-Term to Long-Term Memory."

---

### Context

**What it is:**
The set of information available to NOVA at a given moment that informs its decisions. Context includes the current Goal, Session history, relevant Memory, active Environment, and user preferences.

**Usage:**
> "The Planner Engine loaded the full Context before generating the Plan."

---

### Knowledge Base

**What it is:**
A structured store of facts, documents, and domain-specific information that NOVA can query to enrich its reasoning. Distinct from Memory (which is personal/session-based).

**Usage:**
> "The Research Skill queries the Knowledge Base for relevant documentation before planning."

---

## 7. Configuration & Policy

These terms describe how NOVA is controlled and governed.

---

### Permission

**What it is:**
An explicit grant that allows NOVA to perform a specific category of Action or invoke a specific Tool. Permissions are defined in the Permission Policy and enforced by the Permission Service.

**Key property:**
No Action or Tool invocation proceeds without a valid Permission grant. This is non-negotiable.

**Usage:**
> "The `file_write` Permission is required before NOVA may write to the filesystem."

---

### Permission Policy

**What it is:**
The complete set of rules that govern what NOVA is and is not allowed to do. Permission Policies are user-configurable and can be scoped to Sessions, Workflows, or Tools.

**Usage:**
> "The Permission Policy prohibits file deletion without explicit user confirmation."

---

### Configuration

**What it is:**
The set of named, externalized values that control NOVA's behavior without requiring code changes. All Configuration is stored in the Settings Service and loaded at runtime. Hard-coded values are prohibited.

**Examples:**
- Active Model Provider
- Default language
- Memory retention window
- Enabled Capabilities

**Usage:**
> "The active Model Provider is read from Configuration, not hard-coded."

---

### Policy

**What it is:**
A named rule or set of rules that governs NOVA's behavior in a specific domain. Policies are more general than Permissions. Examples include security policies, data retention policies, and execution policies.

**Usage:**
> "The Execution Policy requires all destructive Actions to request user confirmation."

---

## 8. Observability

These terms describe how NOVA's behavior is monitored and audited.

---

### Audit Log

**What it is:**
An immutable, append-only record of all significant Platform events, particularly all Action executions, Tool invocations, Permission checks, and Plan executions. The Audit Log is the primary accountability artifact.

**Key property:**
The Audit Log cannot be modified or deleted by Platform code. It is write-only from NOVA's perspective.

**Usage:**
> "Every Tool invocation is written to the Audit Log before execution begins."

---

### Event

**What it is:**
A structured, named occurrence within the Platform that is emitted by a component and can be consumed by other components or logged. Events are the primary communication mechanism between decoupled components.

**Examples:**
- `PlanStarted`
- `TaskCompleted`
- `ActionFailed`
- `PermissionDenied`
- `SessionEnded`

**Usage:**
> "The Planner Engine emits a `PlanStarted` Event when a Plan begins execution."

---

### Trace

**What it is:**
A linked sequence of Events that together represent a single end-to-end execution path through the Platform. Traces are used to debug, profile, and audit complex multi-step operations.

**Usage:**
> "The Trace showed that the Plan failed at the `File Write` Task due to a Permission denial."

---

### Metric

**What it is:**
A quantitative measurement of Platform behavior over time. Metrics are used for performance monitoring, reliability tracking, and capacity planning.

**Examples:**
- Average Plan generation latency
- Action success rate
- Memory retrieval time
- Session duration

**Usage:**
> "The Metrics dashboard showed a 15% increase in average Plan generation latency after the last deployment."

---

## 9. Development & Process

These terms describe the engineering process and workflow.

---

### Commission

**What it is:**
The formal act of assigning an engineering task to Antigravity (Lead Software Engineering Agent). A Commission includes a Specification, Architecture context, Interfaces, Tests, and Acceptance Criteria. It replaces informal requests like "build X."

**Format:**
```
Commission
[Document ID]
[Capability or Component Name]
```

**Example:**
```
Commission
NOVA-VISION-001
Desktop OCR Capability
```

**Usage:**
> "The Chief Architect issued Commission NOVA-VISION-001 to Antigravity."

---

### Specification

**What it is:**
A formal document that precisely describes what a component must do, how it must behave, and what its interfaces must look like. Specifications precede implementation. Antigravity does not begin implementation without a Specification.

**Usage:**
> "The Specification for NOVA-VISION-001 defines the OCR Service interface and error handling requirements."

---

### Acceptance Criteria

**What it is:**
The explicit, testable conditions that must be satisfied for a Commission to be considered complete. Acceptance Criteria are defined in the Specification and verified by the Project Founder.

**Usage:**
> "Acceptance Criteria for NOVA-VISION-001 include: OCR accuracy ≥ 95% on standard desktop fonts."

---

### Architectural Review

**What it is:**
The process by which the Chief Architect evaluates a completed implementation for compliance with the approved Architecture, Engineering Standards, and Specifications before it is merged.

**Usage:**
> "Antigravity submitted the Vision Engine for Architectural Review after completing all unit tests."

---

## 10. Document Types

These are the formal document categories used in Project NOVA.

---

| Abbreviation | Full Name | Purpose |
|---|---|---|
| **PRS** | Product Requirements Specification | Defines what NOVA must do from a product perspective |
| **SRS** | Software Requirements Specification | Defines what the software system must do technically |
| **HLD** | High Level Design | Defines the overall architecture and component relationships |
| **LLD** | Low Level Design | Defines the detailed design of a specific component |
| **ADR** | Architecture Decision Record | Documents a significant architectural decision and its rationale |
| **NES** | NOVA Engineering Standard | Defines a mandatory engineering practice |
| **NCS** | NOVA Coding Standard | Defines mandatory code style and quality rules |
| **NTS** | NOVA Testing Standard | Defines mandatory testing requirements and practices |
| **API** | API Specification | Defines the interface contract for a Service or Engine |
| **RFC** | Request for Comments | A proposal for discussion before a decision is made |
| **GLOSS** | Glossary | This document. The canonical vocabulary reference |
| **ONBOARD** | Onboarding Document | Orientation material for a new team member |

---

### Document ID Format

All NOVA documents follow this ID format:

```
NOVA-[TYPE]-[NUMBER]

Examples:
NOVA-GLOSS-001
NOVA-PRS-001
NOVA-HLD-001
NOVA-ADR-001
NOVA-VISION-001  (Commission)
```

---

## 11. Roles

These are the named roles within Project NOVA.

---

| Role | Holder | Responsibilities |
|---|---|---|
| **Project Founder** | Praveen | Product Vision, Prioritization, Testing, Approval |
| **Chief Architect** | ChatGPT | Architecture, Product Design, AI Design, Security Design, Engineering Standards, Documentation, Reviews, Technical Direction |
| **Lead Software Engineering Agent** | Antigravity | Implementation, Refactoring, Testing, Integration, Bug Fixes, Performance Optimization |

---

## 12. Status Terms

These are the canonical status values used across all NOVA documents and components.

---

| Status | Meaning |
|---|---|
| `DRAFT` | Being authored. Not ready for review. |
| `UNDER REVIEW` | Submitted for Architectural Review. Awaiting feedback. |
| `APPROVED` | Reviewed and approved. May be implemented or published. |
| `ACTIVE` | Currently in use or in execution. |
| `DEPRECATED` | No longer recommended. Retained for reference only. |
| `SUPERSEDED` | Replaced by a newer document or component. Reference the replacement. |
| `REJECTED` | Did not pass review. Must not be implemented. |
| `COMPLETED` | Work is finished and accepted. |
| `FAILED` | Execution resulted in an unrecoverable error. |
| `CANCELLED` | Intentionally stopped before completion. |

---

## Appendix A — Prohibited Terminology

The following terms must **not** be used within NOVA documentation or code without explicit mapping to a defined Glossary term. Using undefined terms creates ambiguity.

| Prohibited Term | Use Instead |
|---|---|
| `module` (ambiguous) | `Module` (NOVA definition), or specify Python `module` explicitly if referring to a file |
| `component` (generic) | `Engine`, `Service`, `Module`, `Adapter`, or `Plugin` |
| `system` (vague) | `Platform`, `Engine`, or specific named system |
| `script` | `Tool`, `Action`, or `Workflow` |
| `bot` | `Platform` or specific Capability name |
| `agent` | Use the role name (e.g., `Planner Engine`, or the named Agent role) |
| `feature` | `Capability`, `Skill`, or `Workflow` |
| `plugin` (unqualified) | `Plugin` (NOVA definition, with Plugin Interface contract) |
| `API` (ambiguous) | `Service API`, `Engine API`, or `Tool Interface` |

---

## Appendix B — Quick Reference Card

```
GOAL          →  What the user wants
INTENTION     →  Structured interpretation of a Goal
PLAN          →  Sequence of Tasks from an Intention
TASK          →  Discrete unit of work in a Plan
ACTION        →  Atomic OS-level operation
WORKFLOW      →  Saved, named, reusable Plan
SKILL         →  User-facing Capability composition
CAPABILITY    →  Platform ability (declarative)
ENGINE        →  Major stateful AI/execution subsystem
SERVICE       →  Stateless backend function provider
MODULE        →  Testable unit within an Engine or Service
TOOL          →  External executable component
ADAPTER       →  Interface bridge to external systems
PROVIDER      →  External AI/data supplier
PLUGIN        →  Optional Platform extension
ENVIRONMENT   →  Context of execution (Desktop, Browser, etc.)
MEMORY        →  Context storage across Sessions
SESSION       →  Session-scoped interaction
PERMISSION    →  Explicit right to perform an Action
COMMISSION    →  Formal engineering task assignment
```

---

*End of Document — NOVA-GLOSS-001 v1.0*

*This document is part of the permanent engineering history of Project NOVA.*
