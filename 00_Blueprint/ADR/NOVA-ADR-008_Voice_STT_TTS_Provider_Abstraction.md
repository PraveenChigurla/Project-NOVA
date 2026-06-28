# Architecture Decision Record
## NOVA-ADR-008: Voice STT and TTS Provider Abstraction Layer

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-008 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CAP-VOI-006 |

---

## 1. Context

NOVA requires speech-to-text (STT) transcription and text-to-speech (TTS) voice generation. These can be executed locally (Whisper, Vosk, Piper) or via API endpoints (Azure, Google Speech). The platform must remain decoupled from specific providers to support offline-first operations, preserve latency limits, and allow swapping.

---

## 2. Decision

We will introduce a **Voice Provider Interface layer** in `01_Source/capabilities/voice.py`.
- Audio transcription engines must implement the **`ISTTProvider`** interface.
- Voice synthesis engines must implement the **`ITTSProvider`** interface.

The interfaces will declare the following contracts:
```python
class ISTTProvider(ABC):
    @abstractmethod
    def transcribe_stream(self, audio_generator: Generator[bytes, None, None]) -> Generator[str, None, None]: ...
    # Yields transcribed text tokens in real time.
    @abstractmethod
    def transcribe_file(self, file_path: str) -> dict: ...
    # Returns complete transcribed text and confidence score: {"text": "...", "confidence": 0.94}

class ITTSProvider(ABC):
    @abstractmethod
    def synthesize_speech(self, text: str, voice_profile: str) -> bytes: ...
    # Returns raw synthesized audio bytes (typically WAV/MP3 format).
```

---

## 3. Rationale

This satisfies the "Model independence" and "Offline-first" principles of the Constitution (`NOVA-002`), ensuring that local Piper and local Whisper instances can be swapped for Azure APIs with only configuration file changes.

---

## 4. Consequences

### Positive
- Framework decoupling: Audio processing libraries (like PyAudio, sounddevice) are isolated inside their tool wrapper classes.
- Zero business logic modifications during voice engine replacements.

### Negative
- Requires maintaining custom audio chunk streaming queues in python, which can introduce threading overhead.
