"""
AetherFlow 配置管理系统

支持YAML配置文件、环境变量、命令行参数三层覆盖。
借鉴OpenClaw的本地优先设计哲学。
"""
import os
import yaml
from pathlib import Path
from dataclasses import dataclass,field
from typing import Optional

DEFAULT_CONFIG_YAML="""# AetherFlow 默认配置
gateway:
  host: 127.0.0.1
  port: 18789
  ws_heartbeat: 30

agents:
  claude-code:
    type: claude
    priority: 1
    max_concurrent: 5
  codex:
    type: openai
    priority: 2
    max_concurrent: 10
  gemini:
    type: google
    priority: 3
    max_concurrent: 10
  hermes:
    type: nous
    priority: 4
    max_concurrent: 3

cost_optimizer:
  budget_monthly: 500
  auto_downgrade: true
  cache_enabled: true
  cache_ttl: 3600
  price_sources:
    - anthropic
    - openai
    - google

quality_engine:
  originality_threshold: 0.6
  auto_enhance: true
  style_presets:
    - professional
    - creative
    - academic
    - technical
  detection_layers:
    - phrase_level
    - structure_level
    - semantic_level

content_sync:
  platforms:
    - wechat
    - zhihu
    - juejin
    - csdn
    - medium
    - devto
  schedule:
    enabled: false
    timezone: Asia/Shanghai

data_layer:
  db_path: ~/.aetherflow/data.db
  vector_store: ~/.aetherflow/vectors
  knowledge_graph: ~/.aetherflow/kgraph

memory:
  persistent: true
  max_history: 1000
  embedding_model: text-embedding-3-small
"""

@dataclass
class GatewayConfig:
    host:str="127.0.0.1"
    port:int=18789
    ws_heartbeat:int=30

@dataclass
class AgentConfig:
    type:str=""
    priority:int=99
    max_concurrent:int=5

@dataclass
class CostOptimizerConfig:
    budget_monthly:float=500.0
    auto_downgrade:bool=True
    cache_enabled:bool=True
    cache_ttl:int=3600
    price_sources:list=field(default_factory=lambda:["anthropic","openai","google"])

@dataclass
class QualityEngineConfig:
    originality_threshold:float=0.6
    auto_enhance:bool=True
    style_presets:list=field(default_factory=lambda:["professional","creative","academic","technical"])
    detection_layers:list=field(default_factory=lambda:["phrase_level","structure_level","semantic_level"])

@dataclass
class ContentSyncConfig:
    platforms:list=field(default_factory=list)
    schedule_enabled:bool=False
    timezone:str="Asia/Shanghai"

@dataclass
class DataLayerConfig:
    db_path:str="~/.aetherflow/data.db"
    vector_store:str="~/.aetherflow/vectors"
    knowledge_graph:str="~/.aetherflow/kgraph"

@dataclass
class MemoryConfig:
    persistent:bool=True
    max_history:int=1000
    embedding_model:str="text-embedding-3-small"

@dataclass
class AetherFlowConfig:
    gateway:GatewayConfig=field(default_factory=GatewayConfig)
    agents:dict=field(default_factory=dict)
    cost_optimizer:CostOptimizerConfig=field(default_factory=CostOptimizerConfig)
    quality_engine:QualityEngineConfig=field(default_factory=QualityEngineConfig)
    content_sync:ContentSyncConfig=field(default_factory=ContentSyncConfig)
    data_layer:DataLayerConfig=field(default_factory=DataLayerConfig)
    memory:MemoryConfig=field(default_factory=MemoryConfig)

def load_config(config_path:Optional[str]=None)->AetherFlowConfig:
    """加载配置：默认值 → 配置文件 → 环境变量"""
    config_data=yaml.safe_load(DEFAULT_CONFIG_YAML)

    if config_path and Path(config_path).exists():
        with open(config_path,"r",encoding="utf-8") as f:
            user_config=yaml.safe_load(f)
            if user_config:
                _deep_merge(config_data,user_config)

    _apply_env_overrides(config_data)

    return _parse_config(config_data)

def _deep_merge(base:dict,override:dict):
    """深度合并配置字典"""
    for key,value in override.items():
        if key in base and isinstance(base[key],dict) and isinstance(value,dict):
            _deep_merge(base[key],value)
        else:
            base[key]=value

def _apply_env_overrides(config:dict):
    """环境变量覆盖配置"""
    env_map={
        "AETHERFLOW_HOST":"gateway.host",
        "AETHERFLOW_PORT":"gateway.port",
        "AETHERFLOW_BUDGET":"cost_optimizer.budget_monthly",
    }
    for env_key,config_path in env_map.items():
        val=os.environ.get(env_key)
        if val:
            keys=config_path.split(".")
            target=config
            for k in keys[:-1]:
                target=target.setdefault(k,{})
            target[keys[-1]]=type(target.get(keys[-1],""))(val)

def _parse_config(data:dict)->AetherFlowConfig:
    """将字典解析为类型化配置对象"""
    return AetherFlowConfig(
        gateway=GatewayConfig(**data.get("gateway",{})),
        agents={k:AgentConfig(**v) for k,v in data.get("agents",{}).items()},
        cost_optimizer=CostOptimizerConfig(**data.get("cost_optimizer",{})),
        quality_engine=QualityEngineConfig(**data.get("quality_engine",{})),
        content_sync=ContentSyncConfig(**data.get("content_sync",{})),
        data_layer=DataLayerConfig(**data.get("data_layer",{})),
        memory=MemoryConfig(**data.get("memory",{})),
    )
