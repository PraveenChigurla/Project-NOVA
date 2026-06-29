# NOVA Architectural Constitution
**Specification ID:** NOVA-STD-000  
**Status:** IMMUTABLE / FOUNDATIONAL  

This document defines the immutable architectural principles of Project NOVA. These principles guarantee that NOVA remains a deterministic, secure, and observable AI Operating Runtime, regardless of how specific models or automation backends evolve.

---

## The Five Laws of NOVA Intelligence

### Law 1 — Deterministic Execution
> Every action must ultimately be executed by the deterministic runtime, never directly by an LLM.

### Law 2 — Explainable Reasoning
> Every recommendation, plan, optimization, and decision must have an observable chain of evidence.

### Law 3 — Human Sovereignty
> NOVA may suggest, optimize, and recommend—but it never changes persistent behavior without explicit human approval.

### Law 4 — Federated Sovereignty
> Every NOVA runtime is an independent sovereign cognitive system. Cooperation is voluntary, authenticated, policy-governed, and never compromises local authority.

### Law 5 — Knowledge Mobility
> Memory is sovereign and immobile; Knowledge is abstracted, portable, and verifiable. All shared learning must be explicitly packaged and pass through the Trust Framework.

---

## The 10 Architectural Principles

## 1. Deterministic Execution is Authoritative
Execution is not probabilistic. The runtime executes rigidly defined `ExecutionPlans`. The AI reasoning layers generate plans, but the Execution Engine executes them deterministically. 

## 2. LLMs are Advisors, Never Executors
Large Language Models exist strictly as "Cognitive Advisors." They interpret natural language, parse intent, and output structured `GoalContracts`. They must never be granted direct access to `execute()`, bypassing the Planner.

## 3. All Execution Passes Through the Permission Framework
Capabilities cannot execute arbitrary commands. Every request from the Planner must pass through the `PermissionFramework`, ensuring safety boundaries and user consent are enforced before execution.

## 4. The World Model is the Single Source of Truth
Subsystems do not independently query the operating system. Instead, the `ObservationEngine` continuously updates a graph-based `WorldModel`. All cognitive components (Planner, Reasoner, LLM) query this canonical representation of reality.

## 5. Memory Belongs to NOVA, Not the LLM
NOVA is entirely stateless with respect to the LLM. The `MemoryManager` maintains Working, Episodic, Semantic, Procedural, and Knowledge memories locally. The LLM is provided only the precise context required to fulfill the current intent.

## 6. Skills are Portable Packages Compiled into Execution Plans
Functionality is not hardcoded into the runtime. `Skills` compose atomic `Capabilities` into reusable graphs. The `WorkflowCompiler` reduces these skills into a deterministic `ExecutionPlan`.

## 7. Providers Abstract External Technologies
The runtime must never depend on a specific external tool. Web automation is handled via a `WebAutomationProvider` (abstracting Playwright or CDP). AI reasoning is handled via an `LLMProvider` (abstracting OpenAI or Local models). 

## 8. Capabilities Expose Atomic Actions; Skills Compose Them
A `Capability` (e.g., `Mouse.click`) is an atomic primitive provided by the OS or a Provider. A `Skill` (e.g., `GitHub.login`) is a composition of those primitives. Planners orchestrate Skills.

## 9. Every Execution is Observable Through the Event Chronicle
NOVA maintains an append-only `EventChronicle`. Every major lifecycle event (`GoalReceived`, `PlanGenerated`, `ReflectionCompleted`) is recorded immutably. This enables deterministic replay, debugging, and continuous learning.

## 10. Every Subsystem Communicates Through Typed Contracts
Stringly-typed programming is forbidden at module boundaries. The LLM outputs a `GoalContract`. The Cognition Layer outputs a `CognitivePackage`. The Planner outputs an `ExecutionPlan`. Interfaces are strict.
