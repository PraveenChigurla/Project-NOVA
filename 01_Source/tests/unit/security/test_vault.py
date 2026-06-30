"""
Tests for the Secret Vault Framework.
"""
import os
import pytest
from nova.security.vault.core import SecretVault
from nova.security.vault.models import VaultIdentity, VaultCredential, CredentialType

def test_vault_encryption_and_retrieval(tmp_path):
    vault_file = os.path.join(tmp_path, "vault.enc")
    
    # 1. Initialize and Unlock
    vault = SecretVault(storage_path=vault_file)
    vault._salt_path = os.path.join(tmp_path, "vault.salt")
    assert vault.unlock("test_password_123") == True
    
    # 2. Store secret
    identity = VaultIdentity(
        id="test.api",
        credentials={
            "key": VaultCredential(type=CredentialType.API_KEY, value="super_secret_value")
        }
    )
    vault.store(identity)
    
    # 3. Retrieve secret
    val = vault.get_credential("test.api", "key", "test_accessor")
    assert val == "super_secret_value"
    
    # 4. Verify Audit Log
    assert len(vault._audit_log) == 1
    assert vault._audit_log[0].accessor_id == "test_accessor"
    assert vault._audit_log[0].status == "GRANTED"
    
    # 5. Verify physical file exists and doesn't contain plaintext
    assert os.path.exists(vault_file)
    with open(vault_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        assert "super_secret_value" not in content
        
def test_vault_wrong_password(tmp_path):
    vault_file = os.path.join(tmp_path, "vault.enc")
    
    vault = SecretVault(storage_path=vault_file)
    vault._salt_path = os.path.join(tmp_path, "vault.salt")
    vault.unlock("correct_password")
    vault.store(VaultIdentity(id="dummy", credentials={}))
    
    # New instance
    vault2 = SecretVault(storage_path=vault_file)
    vault2._salt_path = vault._salt_path
    
    # Attempt to unlock with wrong password
    assert vault2.unlock("wrong_password") == False
