"""
Tests for Intent Framework.
"""

import pytest
from nova.intelligence.intents.models import Intent, IntentAlias
from nova.intelligence.intents.registry import IntentRegistry
from nova.intelligence.intents.parser import RuleIntentParser

@pytest.fixture
def intent_registry():
    registry = IntentRegistry()
    launch_intent = Intent(
        name="desktop.process.launch",
        required_entities=["application"],
        aliases=[
            IntentAlias(
                pattern=r"(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.]+)",
                entities_map={1: "application"}
            )
        ]
    )
    registry.register(launch_intent)
    return registry

@pytest.fixture
def parser(intent_registry):
    return RuleIntentParser(intent_registry)

@pytest.mark.asyncio
async def test_rule_parser_valid_intent(parser):
    result = await parser.parse("please launch notepad.exe")
    assert result.intent_name == "desktop.process.launch"
    assert result.is_valid is True
    assert result.entities["application"] == "notepad.exe"
    assert result.confidence == 1.0

@pytest.mark.asyncio
async def test_rule_parser_unknown_intent(parser):
    result = await parser.parse("do a backflip")
    assert result.intent_name == "unknown"
    assert result.is_valid is False
    assert result.confidence == 0.0

@pytest.mark.asyncio
async def test_rule_parser_missing_required_entity(parser):
    # This is slightly contrived as regex usually enforces presence, 
    # but if a regex matched without the group, validation would fail.
    # Let's add a loose alias to test validation.
    parser.registry.register(
        Intent(
            name="desktop.process.launch",
            required_entities=["application"],
            aliases=[
                IntentAlias(
                    pattern=r"launch anything",
                    entities_map={} # No entities extracted
                )
            ]
        )
    )
    result = await parser.parse("launch anything")
    assert result.intent_name == "desktop.process.launch"
    assert result.is_valid is False
    assert result.confidence < 1.0
