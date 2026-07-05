"""
技能管理器 - Skill即插即用框架

借鉴Superpowers的SKILL.md标准格式：
- 独立文件夹 + SKILL.md入口
- 兼容Agent Skills开放规范
- 支持版本管理与社区贡献
"""
import os
import json
import logging
import hashlib
from pathlib import Path
from dataclasses import dataclass,field
from typing import Optional
from enum import Enum

logger=logging.getLogger(__name__)

class SkillCategory(Enum):
    CODE="code"
    DOCS="docs"
    CONTENT="content"
    RESEARCH="research"
    BUSINESS="business"
    DESIGN="design"
    CUSTOM="custom"

@dataclass
class SkillMetadata:
    """技能元信息"""
    name:str
    version:str="1.0.0"
    author:str=""
    description:str=""
    category:SkillCategory=SkillCategory.CUSTOM
    tags:list=field(default_factory=list)
    dependencies:list=field(default_factory=list)
    compatible_agents:list=field(default_factory=lambda:["claude-code","codex"])
    entry_file:str="SKILL.md"

@dataclass
class SkillInfo:
    """技能完整信息"""
    metadata:SkillMetadata
    path:Path
    installed_at:float=0.0
    usage_count:int=0
    rating:float=0.0
    enabled:bool=True

class SkillManager:
    """技能管理器——管理内置技能和社区技能"""

    def __init__(self,skills_dir:Path):
        self.skills_dir=Path(skills_dir)
        self._skills:dict[str,SkillInfo]={}
        self._marketplace_cache:list[dict]=[]
        self.skills_dir.mkdir(parents=True,exist_ok=True)
        self._scan_local_skills()

    def install_skill(self,skill_config:dict)->Optional[SkillInfo]:
        """安装技能——从配置创建技能目录结构"""
        name=skill_config.get("name","")
        if not name:
            logger.error("技能名称为空")
            return None
        if name in self._skills:
            logger.warning(f"技能 '{name}' 已安装")
            return self._skills[name]

        skill_dir=self.skills_dir/name
        skill_dir.mkdir(exist_ok=True)

        metadata=SkillMetadata(
            name=name,
            version=skill_config.get("version","1.0.0"),
            author=skill_config.get("author",""),
            description=skill_config.get("description",""),
            category=SkillCategory(skill_config.get("category","custom")),
            tags=skill_config.get("tags",[]),
            dependencies=skill_config.get("dependencies",[]),
            compatible_agents=skill_config.get("compatible_agents",["claude-code","codex"]),
        )

        skill_md_content=skill_config.get("content","")
        if skill_md_content:
            (skill_dir/"SKILL.md").write_text(skill_md_content,encoding="utf-8")

        skill_meta_json={
            "name":metadata.name,
            "version":metadata.version,
            "author":metadata.author,
            "description":metadata.description,
            "category":metadata.category.value,
            "tags":metadata.tags,
            "dependencies":metadata.dependencies,
            "compatible_agents":metadata.compatible_agents,
        }
        (skill_dir/"skill.json").write_text(json.dumps(skill_meta_json,indent=2,ensure_ascii=False),encoding="utf-8")

        info=SkillInfo(metadata=metadata,path=skill_dir)
        self._skills[name]=info
        logger.info(f"技能安装成功: {name} v{metadata.version}")
        return info

    def uninstall_skill(self,name:str)->bool:
        """卸载技能"""
        if name not in self._skills:
            return False
        info=self._skills.pop(name)
        logger.info(f"技能已卸载: {name}")
        return True

    def get_skill(self,name:str)->Optional[SkillInfo]:
        """获取技能信息"""
        return self._skills.get(name)

    def list_skills(self,category:Optional[SkillCategory]=None)->list[SkillInfo]:
        """列出所有技能"""
        skills=list(self._skills.values())
        if category:
            skills=[s for s in skills if s.metadata.category==category]
        return sorted(skills,key=lambda s:s.metadata.name)

    def search_skills(self,query:str)->list[SkillInfo]:
        """搜索技能——按名称、标签、描述匹配"""
        query_lower=query.lower()
        results=[]
        for skill in self._skills.values():
            meta=skill.metadata
            if (query_lower in meta.name.lower() or 
                query_lower in meta.description.lower() or
                any(query_lower in tag.lower() for tag in meta.tags)):
                results.append(skill)
        return results

    def enable_skill(self,name:str)->bool:
        """启用技能"""
        if name in self._skills:
            self._skills[name].enabled=True
            return True
        return False

    def disable_skill(self,name:str)->bool:
        """禁用技能"""
        if name in self._skills:
            self._skills[name].enabled=False
            return True
        return False

    def get_skill_content(self,name:str)->Optional[str]:
        """获取技能的SKILL.md内容"""
        skill=self.get_skill(name)
        if not skill:
            return None
        entry=skill.path/skill.metadata.entry_file
        if entry.exists():
            return entry.read_text(encoding="utf-8")
        return None

    def _scan_local_skills(self):
        """扫描本地已安装技能"""
        if not self.skills_dir.exists():
            return
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            meta_file=skill_dir/"skill.json"
            if not meta_file.exists():
                continue
            try:
                meta_data=json.loads(meta_file.read_text(encoding="utf-8"))
                metadata=SkillMetadata(
                    name=meta_data["name"],
                    version=meta_data.get("version","1.0.0"),
                    author=meta_data.get("author",""),
                    description=meta_data.get("description",""),
                    category=SkillCategory(meta_data.get("category","custom")),
                    tags=meta_data.get("tags",[]),
                    dependencies=meta_data.get("dependencies",[]),
                    compatible_agents=meta_data.get("compatible_agents",[]),
                )
                self._skills[metadata.name]=SkillInfo(metadata=metadata,path=skill_dir)
            except Exception as e:
                logger.warning(f"技能目录解析失败 {skill_dir}: {e}")

    def get_stats(self)->dict:
        """获取技能统计"""
        categories={}
        for skill in self._skills.values():
            cat=skill.metadata.category.value
            categories[cat]=categories.get(cat,0)+1
        return {
            "total_skills":len(self._skills),
            "enabled":sum(1 for s in self._skills.values() if s.enabled),
            "disabled":sum(1 for s in self._skills.values() if not s.enabled),
            "categories":categories,
            "total_usage":sum(s.usage_count for s in self._skills.values()),
        }
