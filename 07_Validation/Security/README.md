# Security Validation

This directory contains adversarial tests against the NOVA architecture.

**Key Objectives:**
*   Fuzz Goal Contracts to test parser resilience.
*   Attempt to bypass the `PermissionFramework` (Privilege Escalation).
*   Test the `TrustFramework` against forged `.nova` and `.kpkg` signatures.
*   Verify that the Secret Vault cannot be accessed via memory dumps or arbitrary Capability execution.
