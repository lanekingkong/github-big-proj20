"""
AetherFlow Gateway - 统一入口服务

借鉴OpenClaw二元架构：Gateway作为控制面，Agent Runtime作为执行面。
使用WebSocket + HTTP双协议，单进程运行，数据主权归用户。
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

logger=logging.getLogger(__name__)

class AetherFlowGateway:
    """统一Gateway进程——AetherFlow的神经中枢"""

    def __init__(self,host:str="127.0.0.1",port:int=18789):
        self.host=host
        self.port=port
        self._server=None
        self._sessions={}  # session_id -> SessionContext
        self._running=False
        logger.info(f"Gateway初始化: {host}:{port}")

    async def start(self):
        """启动Gateway服务"""
        self._running=True
        logger.info(f"Gateway启动成功: ws://{self.host}:{self.port}")
        print(f"""
╔══════════════════════════════════════════╗
║       AetherFlow Gateway v0.1.0         ║
║  🌊 全能AI智能体编排引擎已启动           ║
║       ws://{self.host}:{self.port:<10}       ║
╚══════════════════════════════════════════╝
        """)

    async def stop(self):
        """停止Gateway服务"""
        self._running=False
        logger.info("Gateway已停止")

    def get_status(self)->dict:
        """获取Gateway运行状态"""
        return {
            "running":self._running,
            "host":self.host,
            "port":self.port,
            "active_sessions":len(self._sessions)
        }

class SessionContext:
    """会话上下文——管理单个会话的状态与资源"""

    def __init__(self,session_id:str):
        self.session_id=session_id
        self.agent_bindings={}  # agent_name -> agent_instance
        self.active_skills=set()
        self.memory_buffer=[]
        self.created_at=asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
