import os
import json
import hashlib
import sys

class CertificationVerifier:
    def __init__(self, cert_dir: str = "07_Validation/EVP/Runtime/EVP-CERT-001"):
        self.cert_dir = cert_dir

    def hash_file(self, path):
        hasher = hashlib.sha256()
        try:
            with open(path, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except Exception:
            return "ERROR"

    def verify_hashes(self) -> bool:
        print("[1] Verifying Cryptographic Hashes...")
        hashes_path = os.path.join(self.cert_dir, "hashes.txt")
        if not os.path.exists(hashes_path):
            print("  [FAIL] hashes.txt not found!")
            return False

        passed = True
        with open(hashes_path, 'r') as f:
            for line in f:
                parts = line.strip().split("  ", 1)
                if len(parts) != 2:
                    continue
                expected_hash, rel_path = parts
                actual_path = os.path.join(self.cert_dir, rel_path)
                
                if not os.path.exists(actual_path):
                    print(f"  [FAIL] Missing file: {rel_path}")
                    passed = False
                    continue
                    
                actual_hash = self.hash_file(actual_path)
                if actual_hash != expected_hash:
                    print(f"  [FAIL] Hash mismatch: {rel_path} (Expected: {expected_hash}, Actual: {actual_hash})")
                    passed = False
                else:
                    print(f"  [PASS] {rel_path}")
                    
        return passed

    def verify_metrics(self) -> bool:
        print("\n[2] Verifying Certification Metrics...")
        metrics_path = os.path.join(self.cert_dir, "runtime_metrics.json")
        if not os.path.exists(metrics_path):
            print("  [FAIL] runtime_metrics.json not found!")
            return False

        with open(metrics_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        metrics = data.get("metrics", {})
        total = metrics.get("total_executions", 0)
        unexpected = metrics.get("unexpected_failures", 1)
        
        passed = True
        if total != 100000:
            print(f"  [FAIL] Expected 100000 executions, found {total}")
            passed = False
        else:
            print(f"  [PASS] Executions: 100000")
            
        if unexpected != 0:
            print(f"  [FAIL] Expected 0 unexpected failures, found {unexpected}")
            passed = False
        else:
            print(f"  [PASS] Unexpected Failures: 0")
            
        return passed

    def run(self):
        print("==================================================")
        print(" INDEPENDENT CERTIFICATION VERIFICATION")
        print("==================================================")
        
        if not os.path.exists(self.cert_dir):
            print(f"[FAIL] Certification directory {self.cert_dir} not found.")
            sys.exit(1)

        h_pass = self.verify_hashes()
        m_pass = self.verify_metrics()
        
        print("\n==================================================")
        if h_pass and m_pass:
            print(" VERDICT: CERTIFICATION BUNDLE IS AUTHENTIC & VALID")
            print("==================================================")
            sys.exit(0)
        else:
            print(" VERDICT: CERTIFICATION FAILED OR TAMPERED")
            print("==================================================")
            sys.exit(1)

if __name__ == "__main__":
    verifier = CertificationVerifier()
    verifier.run()
