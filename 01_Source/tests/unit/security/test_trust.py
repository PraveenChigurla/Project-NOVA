"""
Tests for the Trust Policy Engine.
"""
import pytest
from nova.security.trust.models import PackageManifest, PolicyEnvironment
from nova.security.trust.policy import PolicyEngine

def test_enterprise_policy_rejects_vault_access():
    policy = PolicyEngine(PolicyEnvironment.ENTERPRISE)
    
    manifest = PackageManifest(
        name="test",
        version="1.0",
        publisher="test",
        permissions_requested=["vault.read"],
        has_sbom=True
    )
    
    is_allowed, reasons = policy.evaluate(manifest)
    assert is_allowed == False
    assert any("Vault access" in r for r in reasons)

def test_enterprise_policy_requires_sbom():
    policy = PolicyEngine(PolicyEnvironment.ENTERPRISE)
    
    manifest = PackageManifest(
        name="test",
        version="1.0",
        publisher="test",
        permissions_requested=["browser.read"],
        has_sbom=False
    )
    
    is_allowed, reasons = policy.evaluate(manifest)
    assert is_allowed == False
    assert any("SBOM" in r for r in reasons)

def test_personal_policy_allows_vault_access():
    policy = PolicyEngine(PolicyEnvironment.PERSONAL)
    
    manifest = PackageManifest(
        name="test",
        version="1.0",
        publisher="test",
        permissions_requested=["vault.read"],
        has_sbom=False
    )
    
    is_allowed, reasons = policy.evaluate(manifest)
    assert is_allowed == True
