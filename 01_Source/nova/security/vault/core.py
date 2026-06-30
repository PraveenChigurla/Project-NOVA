"""
Secret Vault Core.
Handles encryption at rest, secure retrieval, and immutable auditing.
"""
import os
import json
import time
import logging
import base64
from typing import Dict, Optional, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from nova.security.vault.models import VaultIdentity, VaultCredential, VaultAuditEntry

logger = logging.getLogger(__name__)

class VaultEncryption:
    """Handles AES-128-CBC encryption with HMAC integrity validation."""
    
    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

class SecretVault:
    """The secure enclave for storing and retrieving Identities."""
    
    def __init__(self, storage_path: str = "vault.enc"):
        self.storage_path = storage_path
        self._identities: Dict[str, VaultIdentity] = {}
        self._fernet: Optional[Fernet] = None
        self._audit_log: List[VaultAuditEntry] = []
        self._is_unlocked = False
        self._salt_path = "vault.salt"
        
    @property
    def is_unlocked(self) -> bool:
        return self._is_unlocked
        
    def unlock(self, master_password: str) -> bool:
        """Derives the key and attempts to decrypt the vault."""
        if not os.path.exists(self._salt_path):
            # First time setup
            salt = os.urandom(16)
            with open(self._salt_path, "wb") as f:
                f.write(salt)
        else:
            with open(self._salt_path, "rb") as f:
                salt = f.read()
                
        key = VaultEncryption.derive_key(master_password, salt)
        self._fernet = Fernet(key)
        
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = self._fernet.decrypt(encrypted_data)
                raw_dict = json.loads(decrypted_data.decode('utf-8'))
                
                self._identities = {}
                for k, v in raw_dict.items():
                    self._identities[k] = VaultIdentity(**v)
            except Exception as e:
                logger.error(f"Vault decryption failed (Invalid password or file tampered): {e}")
                return False
                
        self._is_unlocked = True
        logger.info("Secret Vault unlocked securely.")
        return True
        
    def lock(self):
        """Purges decrypted identities from memory."""
        self._identities.clear()
        self._fernet = None
        self._is_unlocked = False
        logger.info("Secret Vault locked. Memory purged.")
        
    def store(self, identity: VaultIdentity) -> None:
        """Stores a new identity and flushes to encrypted disk."""
        if not self._is_unlocked:
            raise RuntimeError("Vault is locked.")
            
        self._identities[identity.id] = identity
        self._flush()
        logger.debug(f"Stored identity '{identity.id}' in Vault.")
        
    def _flush(self) -> None:
        """Encrypts and writes the current memory state to disk."""
        if not self._fernet:
            raise RuntimeError("Cannot flush: No active encryption key.")
            
        raw_dict = {k: v.model_dump() for k, v in self._identities.items()}
        json_data = json.dumps(raw_dict).encode('utf-8')
        encrypted_data = self._fernet.encrypt(json_data)
        
        with open(self.storage_path, "wb") as f:
            f.write(encrypted_data)
            
    def get_credential(self, identity_id: str, credential_key: str, accessor_id: str) -> Optional[str]:
        """
        Secure retrieval of a single secret.
        Requires the accessor_id (e.g. Skill ID) for audit logging.
        """
        if not self._is_unlocked:
            self._audit(identity_id, credential_key, accessor_id, "DENIED (Locked)")
            raise RuntimeError("Vault is locked.")
            
        identity = self._identities.get(identity_id)
        if not identity:
            self._audit(identity_id, credential_key, accessor_id, "DENIED (Identity Not Found)")
            return None
            
        cred = identity.credentials.get(credential_key)
        if not cred:
            self._audit(identity_id, credential_key, accessor_id, "DENIED (Credential Not Found)")
            return None
            
        # Optional: In the future, check VaultPolicy here to ensure accessor_id is allowed to read this identity.
        
        self._audit(identity_id, credential_key, accessor_id, "GRANTED")
        return cred.value
        
    def _audit(self, identity_id: str, credential_key: str, accessor_id: str, status: str):
        """Immutable audit trail."""
        entry = VaultAuditEntry(
            timestamp=time.time(),
            identity_id=identity_id,
            credential_key=credential_key,
            accessor_id=accessor_id,
            status=status
        )
        self._audit_log.append(entry)
        logger.info(f"[VAULT AUDIT] {accessor_id} requested {identity_id}.{credential_key} -> {status}")
