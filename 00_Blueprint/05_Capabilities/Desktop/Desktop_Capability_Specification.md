# Desktop Automation Capability Specification
## Project NOVA Desktop Orchestration, Window Management, and OS Automation Interface

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-SPEC-005 |
| **Version** | 1.0 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-SPEC-001, NOVA-SPEC-002, NOVA-SPEC-003 |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Consolidate Desktop Overview, App Management, Window Control, Mouse/Keyboard Emulation, Screen Capture, Safety, and Test specifications. |

---

## Table of Contents
1. [Purpose & Scope](#purpose--scope)
2. [Application Management](#application-management)
3. [Window Management](#window-management)
4. [Mouse emulation Control](#mouse-emulation-control)
5. [Keyboard emulation Control](#keyboard-emulation-control)
6. [Display Capture & Screen Observation](#display-capture--screen-observation)
7. [Safety, Permissions & Kill Switches](#safety-permissions--kill-switches)
8. [Testing & Verification Suite](#testing--verification-suite)

---

## Purpose & Scope

This specification defines the functional boundaries, API contracts, and safety policies for the **Desktop Automation Capability**. It permits NOVA to open applications, position windows, capture displays, and emulate mouse and keyboard inputs under standard operating system environments.

---

## Application Management

### Functions
*   **Open Application:** Launches a target program at an absolute path with configurable string arguments.
*   **Close Application:** Safely terminates a process given its process identifier (PID).
*   **Focus Application:** Moves a target process window to the foreground.
*   **Detect Running Processes:** Queries the OS process table to return running instances.

### Acceptance Criteria
Applications launch, switch focus, and close reliably, returning structured result objects containing process metadata.

---

## Window Management

The subsystem must wrap window handle operations to manage application displays:
-   **Enumerate Windows:** Returns a list of active application handles, titles, and positions.
-   **Window Control:** Minimizes, maximizes, restores, or resizes window states.
-   **Window Positioning:** Moves window bounds to target display screen coordinates.

---

## Mouse Emulation Control

Provides mouse cursor inputs:
-   **Move Cursor:** Glides mouse coordinates to a target point.
-   **Emulate Clicks:** Performs left clicks, right clicks, double clicks, or drags.
-   **Scroll Wheel:** Emulates mouse wheel rolls (vertical and horizontal).

*Safety constraint:* Mouse inputs must validate coordinates against physical monitor bounds. Off-screen emulations are prohibited.

---

## Keyboard Emulation Control

Provides keyboard input automation:
-   **Type Text:** Emulates key strokes for a target string block.
-   **Key Combinations:** Emulates concurrent key actions (e.g. `Ctrl+C`).
-   **Hotkeys:** Triggers system global hotkeys.
-   **Clipboard Transfers:** Reads and writes text values to the OS clipboard.

---

## Display Capture & Screen Observation

Captures screen pixels for vision processing:
-   **Full Screenshot:** Acquires a PNG buffer of the primary screen.
-   **Region Capture:** Acquires a specific coordinate bounding box.
-   **Active Window Frame:** Captures the focused application window boundary.
-   **Multi-Monitor Support:** Detects multiple connected displays and handles offset coordinates.

*Constraint:* Screen Capture only outputs raw image buffers; it does not parse layouts or execute character recognition (OCR) natively.

---

## Safety, Permissions & Kill Switches

To guarantee safety, the implementation enforces these non-negotiable checks:
1.  **Permission Validation:** All desktop actions check permission grants with the `PermissionEngine` before execution.
2.  **Emergency Abort Hotkey:** A background global listener checks for a dedicated cancel hotkey sequence (**`Ctrl+Alt+Shift+X`**). Triggering this immediately cancels active cursor moves or keyboard inputs and halts execution loops.
3.  **Audit Logs:** Every click, keystroke, process launch, and abort is recorded in the local Audit Log.
4.  **Allow/Deny Filters:** Process directories and command targets are restricted using configurable regex filter files.

---

## Testing & Verification Suite

-   **Unit Tests:** Every module tests process launches and window queries using mock OS API structures.
-   **DPI Scaling Tests:** Verification runners check mouse clicks calibrate correctly under differing OS DPI scaling offsets (e.g. 150% scaling).
-   **Failure Recovery Gaps:** Tests verify the execution engine aborts gracefully if a target application window hangs or crashes.
-   **Multi-Monitor Checks:** Confirms coordinate conversions are safe on secondary display configurations.
