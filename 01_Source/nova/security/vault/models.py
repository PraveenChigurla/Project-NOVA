"""
Secret Vault Models.
Defines schemas for secure credential storage and auditing.
"""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class CredentialType(str, Enum):
    PASSWORD = "password"
    USERNAME = "username"
    API_KEY = "api_key"
    TOKEN = "token"

class VaultCredential(BaseModel):
    """An individual secret value."""
    type: CredentialType
    value: str

class VaultIdentity(BaseModel):
    """A logical grouping of credentials for a specific account or service."""
    id: str = Field(..., description="Unique ID for the identity (e.g., github.main)")
    description: str = Field(default="")
    credentials: Dict[str, VaultCredential] = Field(default_factory=dict)

class VaultAuditEntry(BaseModel):
    """Immutable record of secret access."""
    timestamp: float
    identity_id: str
    credential_key: str
    accessor_id: str = Field(..., description="The Skill or System Component that requested the secret.")
    status: str = Field(..., description="GRANTED or DENIED")
