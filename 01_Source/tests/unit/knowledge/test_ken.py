"""
Tests for the Knowledge Exchange Network (KEN).
"""
import pytest
from nova.knowledge.models import KnowledgePackage, KnowledgeManifest, KnowledgeData
from nova.knowledge.repository import KnowledgeRepository
from nova.knowledge.importer import KnowledgeImporter
from nova.security.trust.framework import TrustFramework
from nova.security.trust.models import PolicyEnvironment

def test_importer_accepts_valid_knowledge():
    trust = TrustFramework(PolicyEnvironment.PERSONAL)
    repo = KnowledgeRepository()
    importer = KnowledgeImporter(trust, repo)
    
    manifest = KnowledgeManifest(
        name="test_opt",
        version="1.0",
        publisher="test",
        permissions_requested=[],
        has_signature=True,
        has_sbom=True,
        evidence_score=0.9
    )
    
    data = KnowledgeData(
        category="test",
        target="test_skill",
        payload={}
    )
    
    pkg = KnowledgePackage(manifest=manifest, data=data, evidence_summary="test")
    
    success = importer.import_package(pkg)
    assert success == True
    assert len(repo.get_all()) == 1

def test_importer_rejects_low_evidence():
    trust = TrustFramework(PolicyEnvironment.PERSONAL)
    repo = KnowledgeRepository()
    importer = KnowledgeImporter(trust, repo)
    
    manifest = KnowledgeManifest(
        name="test_opt",
        version="1.0",
        publisher="test",
        permissions_requested=[],
        has_signature=True,
        has_sbom=True,
        evidence_score=0.2 # Below threshold of 0.5
    )
    
    data = KnowledgeData(
        category="test",
        target="test_skill",
        payload={}
    )
    
    pkg = KnowledgePackage(manifest=manifest, data=data, evidence_summary="test")
    
    success = importer.import_package(pkg)
    assert success == False
    assert len(repo.get_all()) == 0
