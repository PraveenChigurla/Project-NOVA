"""
Screen Interaction Engine (Experience 03)
Orchestrates Vision, OCR, TRE, and Mouse capabilities for semantic interaction.
"""
import time

class ScreenInteractionGoal:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def _mock_capture_and_ocr(self, scroll_count=0) -> list:
        """Mocks the OCR/Vision pipeline returning bounding boxes and text."""
        # Mocks screen state. If we scrolled, the state changes.
        if scroll_count == 0:
            return [
                {"text": "Login", "type": "button", "confidence": 0.98, "box": {"x": 100, "y": 50, "w": 60, "h": 20}, "context": "top navigation"},
                {"text": "Password", "type": "label", "confidence": 0.99, "box": {"x": 200, "y": 200, "w": 80, "h": 20}, "context": "form field"},
                {"text": "Login", "type": "button", "confidence": 0.96, "box": {"x": 200, "y": 250, "w": 60, "h": 20}, "context": "below Password"},
                {"text": "Downloads", "type": "label", "confidence": 0.95, "box": {"x": 10, "y": 500, "w": 80, "h": 20}, "context": "sidebar"},
                {"text": "Save", "type": "button", "confidence": 0.99, "box": {"x": 1000, "y": 10, "w": 50, "h": 20}, "context": "top-right corner"}
            ]
        elif scroll_count == 1:
            return [
                {"text": "Privacy Policy", "type": "link", "confidence": 0.97, "box": {"x": 400, "y": 800, "w": 100, "h": 20}, "context": "footer"}
            ]
        elif scroll_count >= 2:
            return [
                {"text": "Settings", "type": "button", "confidence": 0.99, "box": {"x": 100, "y": 900, "w": 80, "h": 30}, "context": "bottom"}
            ]
        return []

    def _resolve_target(self, target_query: str, ocr_data: list) -> dict:
        """TRE implementation. Handles multiple matches and spatial hints."""
        matches = []
        spatial_hint = None
        
        # Parse spatial hints (e.g. "Login below Password")
        base_target = target_query
        if " below " in target_query:
            parts = target_query.split(" below ")
            base_target = parts[0].strip()
            spatial_hint = "below " + parts[1].strip()
            
        for item in ocr_data:
            if base_target.lower() in item["text"].lower():
                matches.append(item)
                
        # Handle spatial filtering
        if spatial_hint and len(matches) > 1:
            filtered = [m for m in matches if spatial_hint.lower() in m["context"].lower()]
            if filtered:
                return {"status": "resolved", "target": filtered[0]}
                
        if len(matches) == 1:
            return {"status": "resolved", "target": matches[0]}
            
        if len(matches) > 1:
            # Sort by Y coordinate to label Top, Middle, Bottom
            matches = sorted(matches, key=lambda x: x["box"]["y"])
            options = []
            for i, match in enumerate(matches):
                options.append(f"{i+1}. {match['text']} ({match['context']})")
            return {"status": "ambiguous", "matches": matches, "options": options}
            
        return {"status": "not_found"}

    def process_command(self, text: str) -> str:
        text_lower = text.lower().strip()
        report = []
        start_time = time.time()
        
        # Screen Understanding
        if any(q in text_lower for q in ["what do you see", "describe this screen", "summarize this window"]):
            ocr_data = self._mock_capture_and_ocr(0)
            report.append("Goal: Screen Observation")
            report.append("\n\033[96m[Vision Engine & OCR]\033[0m")
            report.append(f"Analyzed {len(ocr_data)} elements:")
            for item in ocr_data:
                report.append(f" - {item['type'].capitalize()} '{item['text']}' at {item['context']}")
            report.append(f"\nExecution Time: {round(time.time() - start_time, 2)}s")
            return "\n".join(report)

        # Scroll Search
        if text_lower.startswith("scroll until "):
            target_query = text_lower.replace("scroll until ", "").strip()
            report.append(f"Goal: Scroll Search ('{target_query}')")
            
            max_scrolls = 5
            found = False
            for scroll in range(max_scrolls):
                report.append(f"✓ Capture & OCR (Frame {scroll})")
                ocr_data = self._mock_capture_and_ocr(scroll)
                res = self._resolve_target(target_query, ocr_data)
                
                if res["status"] == "resolved":
                    report.append(f"✓ Found target: '{res['target']['text']}' (Confidence: {res['target']['confidence']})")
                    report.append(f"✓ Target resolved at {res['target']['box']}")
                    report.append("✓ Execution: Click")
                    found = True
                    break
                else:
                    report.append("✗ Target not found in frame. Scrolling down...")
                    time.sleep(0.1) # Mock scroll delay
                    
            if not found:
                report.append(f"✗ Reached scroll limit ({max_scrolls}). Target not found.")
            report.append(f"\nExecution Time: {round(time.time() - start_time, 2)}s")
            return "\n".join(report)

        # Direct Interaction (Click, Select)
        action = None
        target_query = None
        for verb in ["click", "select", "choose", "double-click", "right-click"]:
            if text_lower.startswith(f"{verb} "):
                action = verb
                target_query = text_lower.replace(f"{verb} ", "").strip()
                break
                
        if action and target_query:
            report.append(f"Goal: Semantic Interaction ({action.capitalize()} '{target_query}')")
            report.append("✓ Capture Screen -> Vision Engine -> OCR")
            ocr_data = self._mock_capture_and_ocr(0)
            
            report.append(f"✓ Target Resolution Engine ('{target_query}')")
            res = self._resolve_target(target_query, ocr_data)
            
            if res["status"] == "not_found":
                report.append("✗ Target not found on current screen.")
                return "\n".join(report)
                
            if res["status"] == "ambiguous":
                report.append("\n\033[93m[Interactive Mode]\033[0m")
                report.append(f"I found {len(res['matches'])} '{target_query}' targets.")
                for opt in res["options"]:
                    # Using color blocks 🟦 🟩 for visual parity with prompt
                    color = "🟦" if "top" in opt else "🟩"
                    report.append(f"{color} {opt}")
                report.append("\nWhich one? (e.g. 'first', 'second', 'below password')")
                report.append("Execution paused.")
                return "\n".join(report)
                
            target = res["target"]
            if target["confidence"] < 0.8:
                report.append("\n\033[91m[Low Confidence Warning]\033[0m")
                report.append(f"Confidence is only {target['confidence']}. Proceed with click? [Y/N]")
                return "\n".join(report)
                
            report.append("✓ Interaction Preview (Highlighting Target for 250ms)")
            time.sleep(0.25)
            report.append(f"✓ Mouse Provider: {action.capitalize()} at {target['box']}")
            
            report.append(f"\nExecution Time: {round(time.time() - start_time, 2)}s")
            return "\n".join(report)

        report.append("✗ Unrecognized screen interaction command.")
        return "\n".join(report)
