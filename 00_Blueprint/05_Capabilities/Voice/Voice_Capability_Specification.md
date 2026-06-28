# Voice & Conversation Capability Specification
## Project NOVA Voice Interaction, Speech Transcription, and Conversation Management

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-SPEC-008 |
| **Version** | 1.0 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Created** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-SPEC-001, NOVA-SPEC-002, NOVA-SPEC-003, NOVA-SPEC-004 |

---

## Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-06-28 | Antigravity | Consolidate Voice Overview, Wake Word, STT, TTS, Conversation Management, and Provider Abstraction specifications. |

---

## Table of Contents
1. [Purpose & Scope](#purpose--scope)
2. [Wake Word Detection & Triggers](#wake-word-detection--triggers)
3. [Speech-to-Text (STT) Subsystem](#speech-to-text-stt-subsystem)
4. [Text-to-Speech (TTS) Subsystem](#text-to-speech-tts-subsystem)
5. [Conversation Manager & Session Context](#conversation-manager--session-context)
6. [Provider Abstraction Interfaces](#provider-abstraction-interfaces)
7. [Latency, Privacy & Interruption Policies](#latency-privacy--interruption-policies)
8. [Testing & Noise Resilience Targets](#testing--noise-resilience-targets)

---

## Purpose & Scope

This specification defines the functional boundaries, API contracts, and safety policies for the **Voice & Conversation Capability**. It enables NOVA to receive audio signals, identify wake triggers, transcribe speech, generate voice playbacks, and track conversational session contexts.

*Constraint:* Voice acts as a communication interface. Conversational planning and intention analysis are handled by the `AIKernel` and `PlannerEngine`.

---

## Wake Word Detection & Triggers

-   **Wake Word:** Listens to continuous audio feeds to match configured hotwords (e.g. *"Hey Nova"*).
-   **Resource Bounds:** Wake word routines must execute locally with minimal CPU loads.
-   **Push-to-Talk:** Exposes trigger methods to manually initiate recording sessions without wake-word monitoring.

---

## Speech-to-Text (STT) Subsystem

-   **Audio Transcription:** Converts incoming microphone signal buffers into text strings.
-   **Streaming Outputs:** Emits transcribed tokens in real-time before sentences complete.
-   **Confidence Metrics:** Assigns probability ratings to transcribed tokens.

---

## Text-to-Speech (TTS) Subsystem

-   **Speech Generation:** Converts output response strings into natural audio buffers.
-   **Voice Profiles:** Supports configurable gender, style, and tone profiles.
-   **Interruptible Playback:** Exposes abort hooks to instantly stop audio hardware playback channels.

---

## Conversation Manager & Session Context

-   **Session History:** Records chat text logs and context tokens.
-   **Context Windowing:** Manages conversational limits by pruning or summarizing oldest logs.
-   **Follow-Up Trees:** Handles unresolved questions and multi-turn loops.

---

## Provider Abstraction Interfaces

To ensure model independence, the capability isolates audio engines behind two interface classes:

```python
class ISTTProvider(ABC):
    @abstractmethod
    def transcribe_stream(self, audio_generator: Generator[bytes, None, None]) -> Generator[str, None, None]: ...
    @abstractmethod
    def transcribe_file(self, file_path: str) -> dict: ...

class ITTSProvider(ABC):
    @abstractmethod
    def synthesize_speech(self, text: str, voice_profile: str) -> bytes: ...
```

*Examples:* Whisper, Vosk, Piper, Coqui, or Azure Speech APIs implement these interfaces.

---

## Latency, Privacy & Interruption Policies

1.  **Conversational Turnaround Latency:** Inbound user audio to outbound TTS playback start latency must be under **1.2 seconds**. To satisfy this, transcription must stream blocks in real-time, allowing intent detection to run before sentences terminate.
2.  **Visual Indicators:** A hardware-independent on-screen indicator (e.g., status tray icon) must highlight when the microphone is recording.
3.  **Speaker Interruption Detection:** If user speech is registered during speaker playback, the system must trigger a `PlaybackInterrupted` event, stop synthesis playback, and toggle back to input recording.

---

## Testing & Noise Resilience Targets

-   **Wake-Word Performance:** False positives must be under 1 per 24 hours of ambient room noises.
-   **STT Word Error Rate (WER):** Target WER must be under 10% under standard office background noises.
-   **Interruption Latency:** Synthesis abort turnaround must take less than 150ms after speech is registered.
