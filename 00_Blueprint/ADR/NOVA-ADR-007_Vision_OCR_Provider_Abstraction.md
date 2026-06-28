# Architecture Decision Record
## NOVA-ADR-007: Vision and OCR Provider Abstraction Layer

---

| Field | Value |
|---|---|
| **Document ID** | NOVA-ADR-007 |
| **Status** | `APPROVED` |
| **Author** | Antigravity (Lead Software Engineering Agent) |
| **Reviewer** | ChatGPT (Chief Architect) |
| **Approved By** | Praveen (Project Founder) |
| **Decided Date** | 2026-06-28 |
| **Last Updated** | 2026-06-28 |
| **Dependencies** | NOVA-CAP-VIS-006 |

---

## 1. Context

NOVA requires optical character recognition (OCR) and visual element grounding. OCR and screen understanding can be satisfied by local, lightweight models (Tesseract, PaddleOCR, EasyOCR) or multimodal LLMs (GPT-4o, Claude Sonnet). The platform must remain decoupled from specific providers to support hybrid offline-first execution and model swaps.

---

## 2. Decision

We will introduce a **Vision and OCR Provider Interface layer** in `01_Source/capabilities/vision.py`.
- Local/API OCR tools must implement the **`IOCRProvider`** interface.
- Multimodal layout models must implement the **`IVisionModelProvider`** interface.

The interfaces will declare the following contracts:
```python
class IOCRProvider(ABC):
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> list[dict]: ...
    # Returns bounding boxes, text strings, and confidence metrics:
    # [{"text": "File", "bbox": (x, y, w, h), "confidence": 0.98}]

class IVisionModelProvider(ABC):
    @abstractmethod
    def detect_elements(self, image_bytes: bytes, categories: list[str]) -> list[dict]: ...
    # Returns grounded layout targets:
    # [{"label": "button", "center": (x, y), "bbox": (x1, y1, x2, y2)}]
```

---

## 3. Rationale

This satisfies the "Model independence" and "Offline-first" principles of the Constitution (`NOVA-002`), allowing local Tesseract execution when offline and routing to GPT-4o for complex grounding tasks when online.

---

## 4. Consequences

### Positive
- Framework decoupling: Tesseract or PaddleOCR are completely isolated inside their wrapper services.
- Hybrid execution: The platform can fall back to local OCR when API endpoints fail.

### Negative
- Local models (PaddleOCR/Tesseract) require compiling specific binaries (C++ libs) depending on the user's OS. These must be dynamically loaded.
