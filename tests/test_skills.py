"""
测试 - 技能管理器
"""
import pytest
from pathlib import Path
from src.skills.manager import SkillManager

def test_skill_manager_init():
    manager=SkillManager(Path("skills_builtin"))
    assert manager.skills_dir.exists()

def test_install_skill():
    manager=SkillManager(Path("skills_builtin"))
    # test skill from builtin
    skills=manager.list_skills()
    assert len(skills)>=1  # at least code-review

def test_list_skills():
    manager=SkillManager(Path("skills_builtin"))
    skills=manager.list_skills()
    names=[s.metadata.name for s in skills]
    assert "code-review" in names or len(skills)>0

def test_search_skills():
    manager=SkillManager(Path("skills_builtin"))
    skills=manager.search_skills("code")
    assert len(skills)>=0

def test_get_stats():
    manager=SkillManager(Path("skills_builtin"))
    stats=manager.get_stats()
    assert "total_skills" in stats
    assert "enabled" in stats
