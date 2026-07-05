"""
测试 - Agent注册中心
"""
import pytest
from src.agents.registry import AgentRegistry,AgentInfo,AgentType,AgentCapability,AgentStatus

def test_register_agent():
    registry=AgentRegistry()
    info=AgentInfo(
        name="test-claude",
        agent_type=AgentType.CLAUDE,
        priority=10,
        capabilities=AgentCapability(text=["code"],vision=["diagram"]),
    )
    success=registry.register(info)
    assert success
    assert "test-claude" in registry.list_agents_names()

def test_register_duplicate():
    registry=AgentRegistry()
    info=AgentInfo(name="dup",agent_type=AgentType.CLAUDE,priority=10,capabilities=AgentCapability())
    registry.register(info)
    assert not registry.register(info)

def test_find_best_agent():
    registry=AgentRegistry()
    registry.register(AgentInfo(name="premium",agent_type=AgentType.CLAUDE,priority=1,capabilities=AgentCapability(text=["code","analysis"])))
    registry.register(AgentInfo(name="standard",agent_type=AgentType.CODEX,priority=50,capabilities=AgentCapability(text=["code"])))

    agent=registry.find_best_agent("帮我分析代码")
    assert agent is not None
    assert agent.name in ["premium","standard"]

def test_disable_agent():
    registry=AgentRegistry()
    registry.register(AgentInfo(name="to_disable",agent_type=AgentType.GEMINI,priority=99,capabilities=AgentCapability()))
    assert registry.set_agent_status("to_disable",AgentStatus.OFFLINE)
    assert not registry.set_agent_status("nonexistent",AgentStatus.OFFLINE)

def test_get_stats():
    registry=AgentRegistry()
    registry.register(AgentInfo(name="a1",agent_type=AgentType.CLAUDE,priority=1,capabilities=AgentCapability()))
    registry.register(AgentInfo(name="a2",agent_type=AgentType.CODEX,priority=2,capabilities=AgentCapability()))
    stats=registry.get_stats()
    assert stats["total_agents"]==2
    assert stats["online"]==2
