"""
Agent注册中心 - 统一管理多个AI Agent

借鉴OpenClaw的多渠道接入模式，统一管理Claude Code/Codex/Gemini/Hermes等Agent。
支持动态注册、发现、优先级路由。
"""
import asyncio
import logging
from enum import Enum
from dataclasses import dataclass,field
from typing import Optional,Callable

logger=logging.getLogger(__name__)

class AgentType(Enum):
    CLAUDE="claude"
    CODEX="openai"
    GEMINI="google"
    HERMES="nous"
    CUSTOM="custom"

class AgentStatus(Enum):
    ONLINE="online"
    OFFLINE="offline"
    BUSY="busy"
    ERROR="error"

@dataclass
class AgentCapability:
    """Agent能力描述"""
    code_generation:bool=True
    code_review:bool=True
    file_operations:bool=False
    web_browsing:bool=False
    shell_execution:bool=False
    image_understanding:bool=False
    multimodal:bool=False

@dataclass
class AgentInfo:
    """Agent元信息"""
    name:str
    agent_type:AgentType
    version:str="1.0.0"
    priority:int=99
    max_concurrent:int=5
    capabilities:AgentCapability=field(default_factory=AgentCapability)
    status:AgentStatus=AgentStatus.OFFLINE
    endpoint:Optional[str]=None
    metadata:dict=field(default_factory=dict)

class AgentRegistry:
    """Agent注册中心——管理所有已注册的AI Agent"""

    def __init__(self):
        self._agents:dict[str,AgentInfo]={}
        self._active_sessions:dict[str,int]={}  # agent_name -> active_count
        self._hooks:dict[str,list[Callable]]={"on_register":[],"on_unregister":[],"on_status_change":[]}

    def register(self,info:AgentInfo)->bool:
        """注册新Agent"""
        if info.name in self._agents:
            logger.warning(f"Agent '{info.name}' 已存在，跳过注册")
            return False
        self._agents[info.name]=info
        self._active_sessions[info.name]=0
        info.status=AgentStatus.ONLINE
        self._trigger_hooks("on_register",info)
        logger.info(f"Agent注册成功: {info.name} [{info.agent_type.value}]")
        return True

    def unregister(self,name:str)->bool:
        """注销Agent"""
        if name not in self._agents:
            return False
        info=self._agents.pop(name)
        self._active_sessions.pop(name,None)
        self._trigger_hooks("on_unregister",info)
        logger.info(f"Agent已注销: {name}")
        return True

    def get_agent(self,name:str)->Optional[AgentInfo]:
        """获取Agent信息"""
        return self._agents.get(name)

    def find_best_agent(self,task_type:str,required_caps:Optional[AgentCapability]=None)->Optional[AgentInfo]:
        """智能匹配最优Agent——按优先级+能力匹配"""
        candidates=[]
        for agent in self._agents.values():
            if agent.status!=AgentStatus.ONLINE:
                continue
            if self._active_sessions.get(agent.name,0)>=agent.max_concurrent:
                continue
            score=agent.priority
            if required_caps:
                score+=self._capability_match_score(agent.capabilities,required_caps)
            candidates.append((score,agent))

        if not candidates:
            return None

        candidates.sort(key=lambda x:x[0])
        return candidates[0][1]

    def list_agents(self,status_filter:Optional[AgentStatus]=None)->list[AgentInfo]:
        """列出所有Agent"""
        agents=list(self._agents.values())
        if status_filter:
            agents=[a for a in agents if a.status==status_filter]
        return sorted(agents,key=lambda a:a.priority)

    def update_status(self,name:str,status:AgentStatus):
        """更新Agent状态"""
        if name in self._agents:
            old_status=self._agents[name].status
            self._agents[name].status=status
            if old_status!=status:
                self._trigger_hooks("on_status_change",self._agents[name])

    def on(self,event:str,callback:Callable):
        """注册事件钩子"""
        if event in self._hooks:
            self._hooks[event].append(callback)

    def _trigger_hooks(self,event:str,agent:AgentInfo):
        for cb in self._hooks.get(event,[]):
            try:
                cb(agent)
            except Exception as e:
                logger.error(f"Hook执行失败 [{event}]: {e}")

    def _capability_match_score(self,agent_caps:AgentCapability,required:AgentCapability)->int:
        """计算能力匹配分数（越低越好，0=完美匹配）"""
        score=0
        for attr in ["code_generation","code_review","file_operations","web_browsing","shell_execution","image_understanding","multimodal"]:
            required_val=getattr(required,attr,False)
            agent_val=getattr(agent_caps,attr,False)
            if required_val and not agent_val:
                score+=10
        return score

    def get_stats(self)->dict:
        """获取注册中心统计信息"""
        total=len(self._agents)
        online=sum(1 for a in self._agents.values() if a.status==AgentStatus.ONLINE)
        busy=sum(1 for a in self._agents.values() if a.status==AgentStatus.BUSY)
        return {
            "total_agents":total,
            "online":online,
            "busy":busy,
            "offline":total-online,
            "active_sessions":sum(self._active_sessions.values()),
            "agent_types":{t.value:sum(1 for a in self._agents.values() if a.agent_type.value==t.value) for t in AgentType}
        }
