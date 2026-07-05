"""
示例1：Agent注册与任务编排
演示如何注册Agent、创建编排计划、并行执行任务
"""
import asyncio
from src.agents.registry import AgentRegistry,AgentInfo,AgentType,AgentCapability
from src.orchestrator.router import TaskOrchestrator
from src.skills.manager import SkillManager
from pathlib import Path

async def main():
    # 1. 初始化Agent注册中心
    registry=AgentRegistry()

    # 注册多种Agent
    registry.register(AgentInfo(
        name="claude-sonnet",
        agent_type=AgentType.CLAUDE,
        priority=10,
        capabilities=AgentCapability(text=["code","analysis","writing","qa"])
    ))
    registry.register(AgentInfo(
        name="codex-dev",
        agent_type=AgentType.CODEX,
        priority=20,
        capabilities=AgentCapability(text=["code","debug","test"])
    ))
    registry.register(AgentInfo(
        name="gemini-vision",
        agent_type=AgentType.GEMINI,
        priority=30,
        capabilities=AgentCapability(text=["qa"],vision=["diagram","chart"])
    ))

    print("已注册Agent:")
    for agent in registry.list_agents():
        print(f"  [{agent.priority}] {agent.name} ({agent.agent_type.value})")

    # 2. 初始化技能管理器
    skills=SkillManager(Path("skills_builtin"))
    print(f"\n已加载技能: {len(skills.list_skills())}")

    # 3. 创建编排器
    orchestrator=TaskOrchestrator(registry,skills)

    # 4. 创建任务编排计划
    plan=orchestrator.create_plan(
        task_description="构建一个Python Web API项目：包含用户认证、CRUD接口、Swagger文档",
        subtasks=[
            {
                "name":"设计API架构",
                "description":"设计RESTful API端点、数据模型和认证流程",
                "agent_type":"auto",
                "priority":2,
            },
            {
                "name":"实现用户认证",
                "description":"实现JWT认证逻辑、登录/注册接口",
                "agent_type":"auto",
                "priority":2,
            },
            {
                "name":"生成CRUD代码",
                "description":"根据数据模型生成完整的CRUD接口代码",
                "agent_type":"auto",
                "priority":1,
            },
            {
                "name":"编写API文档",
                "description":"生成Swagger/OpenAPI文档",
                "agent_type":"auto",
                "priority":1,
            },
        ]
    )

    # 5. 执行编排计划
    print(f"\n执行编排计划: {plan.plan_id} ({len(plan.tasks)}个子任务)")
    results=await orchestrator.execute_plan(plan)
    print(f"  完成: {results['completed']} | 失败: {results['failed']}")

    # 6. 查看状态
    status=orchestrator.get_plan_status(plan.plan_id)
    print(f"  计划状态: {status}")

if __name__=="__main__":
    asyncio.run(main())
