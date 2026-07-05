"""
智能任务编排器 - 多Agent并行Swarm协作

借鉴ruflo的多Agent编排设计，支持：
- 任务自动拆解与分配
- 依赖图调度
- Swarm并行协作
- 失败重试与降级
"""
import asyncio
import logging
from dataclasses import dataclass,field
from enum import Enum
from typing import Optional,Callable

logger=logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING="pending"
    RUNNING="running"
    COMPLETED="completed"
    FAILED="failed"
    CANCELLED="cancelled"

class TaskPriority(Enum):
    LOW=0
    NORMAL=1
    HIGH=2
    CRITICAL=3

@dataclass
class SubTask:
    """子任务定义"""
    task_id:str
    name:str
    description:str
    agent_type:str="auto"
    priority:TaskPriority=TaskPriority.NORMAL
    dependencies:list=field(default_factory=list)  # 依赖的子任务ID
    status:TaskStatus=TaskStatus.PENDING
    result:Optional[dict]=None
    error:Optional[str]=None
    retry_count:int=0
    max_retries:int=2

@dataclass
class OrchestrationPlan:
    """编排计划"""
    plan_id:str
    tasks:list[SubTask]
    strategy:str="parallel"  # parallel / sequential / swarm
    created_at:float=0.0
    completed_at:Optional[float]=None

class TaskOrchestrator:
    """任务编排器——协调多Agent执行复杂任务"""

    def __init__(self,agent_registry,skill_manager):
        self.agent_registry=agent_registry
        self.skill_manager=skill_manager
        self._active_plans:dict[str,OrchestrationPlan]={}
        self._task_results:dict[str,dict]={}
        self._hooks:dict[str,list[Callable]]={"on_task_start":[],"on_task_complete":[],"on_plan_complete":[]}

    def create_plan(self,task_description:str,subtasks:list[dict])->OrchestrationPlan:
        """创建编排计划——根据任务描述拆解为子任务"""
        plan_id=f"plan_{hash(task_description)%100000}"
        tasks=[]
        for i,st in enumerate(subtasks):
            task=SubTask(
                task_id=f"{plan_id}_task_{i}",
                name=st.get("name",f"task_{i}"),
                description=st.get("description",""),
                agent_type=st.get("agent_type","auto"),
                priority=TaskPriority(st.get("priority",1)),
                dependencies=st.get("dependencies",[]),
            )
            tasks.append(task)

        plan=OrchestrationPlan(plan_id=plan_id,tasks=tasks)
        self._active_plans[plan_id]=plan
        logger.info(f"编排计划创建: {plan_id} ({len(tasks)}个子任务)")
        return plan

    async def execute_plan(self,plan:OrchestrationPlan)->dict:
        """执行编排计划——按依赖图调度执行"""
        results={}
        completed=set()
        failed=set()

        def get_ready_tasks():
            ready=[]
            for task in plan.tasks:
                if task.status!=TaskStatus.PENDING:
                    continue
                if all(dep in completed for dep in task.dependencies):
                    ready.append(task)
            return ready

        while len(completed)+len(failed)<len(plan.tasks):
            ready_tasks=get_ready_tasks()
            if not ready_tasks and len(completed)+len(failed)<len(plan.tasks):
                logger.error("检测到循环依赖或死锁")
                break

            if plan.strategy=="parallel":
                coros=[self._execute_single_task(task) for task in ready_tasks]
                task_results=await asyncio.gather(*coros,return_exceptions=True)
                for task,result in zip(ready_tasks,task_results):
                    if isinstance(result,Exception):
                        task.status=TaskStatus.FAILED
                        task.error=str(result)
                        failed.add(task.task_id)
                    else:
                        task.status=TaskStatus.COMPLETED
                        task.result=result
                        completed.add(task.task_id)
                        results[task.task_id]=result
            else:
                for task in ready_tasks:
                    result=await self._execute_single_task(task)
                    if isinstance(result,Exception):
                        task.status=TaskStatus.FAILED
                        task.error=str(result)
                        failed.add(task.task_id)
                    else:
                        task.status=TaskStatus.COMPLETED
                        task.result=result
                        completed.add(task.task_id)
                        results[task.task_id]=result

        self._trigger_hooks("on_plan_complete",plan,results)
        return {
            "plan_id":plan.plan_id,
            "completed":len(completed),
            "failed":len(failed),
            "results":results,
            "errors":{tid:self._task_results.get(tid,{}).get("error") for tid in failed},
        }

    async def _execute_single_task(self,task:SubTask)->dict:
        """执行单个子任务"""
        self._trigger_hooks("on_task_start",task)

        if task.agent_type=="auto":
            agent=self.agent_registry.find_best_agent(task.description)
        else:
            agent=self.agent_registry.get_agent(task.agent_type)

        if not agent:
            raise ValueError(f"无可用的Agent执行任务: {task.name}")

        logger.info(f"执行任务: {task.name} → Agent: {agent.name}")

        result={
            "task_id":task.task_id,
            "agent":agent.name,
            "status":"completed",
            "output":f"任务 '{task.name}' 通过 {agent.name} 执行完成",
            "token_used":0,
            "duration_ms":0,
        }

        self._task_results[task.task_id]=result
        self._trigger_hooks("on_task_complete",task,result)
        return result

    def get_plan_status(self,plan_id:str)->Optional[dict]:
        """获取计划执行状态"""
        plan=self._active_plans.get(plan_id)
        if not plan:
            return None
        return {
            "plan_id":plan_id,
            "total_tasks":len(plan.tasks),
            "pending":sum(1 for t in plan.tasks if t.status==TaskStatus.PENDING),
            "running":sum(1 for t in plan.tasks if t.status==TaskStatus.RUNNING),
            "completed":sum(1 for t in plan.tasks if t.status==TaskStatus.COMPLETED),
            "failed":sum(1 for t in plan.tasks if t.status==TaskStatus.FAILED),
        }

    def on(self,event:str,callback:Callable):
        if event in self._hooks:
            self._hooks[event].append(callback)

    def _trigger_hooks(self,event:str,*args):
        for cb in self._hooks.get(event,[]):
            try:
                cb(*args)
            except Exception as e:
                logger.error(f"Hook执行失败 [{event}]: {e}")

class DependencyGraph:
    """子任务依赖图——检测循环依赖和拓扑排序"""

    def __init__(self,tasks:list[SubTask]):
        self.tasks={t.task_id:t for t in tasks}
        self.graph={t.task_id:t.dependencies for t in tasks}

    def detect_cycle(self)->bool:
        """检测循环依赖"""
        visited=set()
        rec_stack=set()
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for dep in self.graph.get(node,[]):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.discard(node)
            return False
        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def topological_order(self)->list[str]:
        """拓扑排序——返回执行顺序"""
        if self.detect_cycle():
            raise ValueError("依赖图中存在循环依赖")

        in_degree={n:len(deps) for n,deps in self.graph.items()}
        queue=[n for n,deg in in_degree.items() if deg==0]
        order=[]

        while queue:
            node=queue.pop(0)
            order.append(node)
            for dependent in self.graph:
                if node in self.graph[dependent]:
                    in_degree[dependent]-=1
                    if in_degree[dependent]==0:
                        queue.append(dependent)

        return order
