"""
AetherFlow CLI - 命令行入口
"""
import sys
import argparse
import asyncio
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(
        prog="aetherflow",
        description="AetherFlow - 全能AI智能体编排与创作品质引擎",
    )
    subparsers=parser.add_subparsers(dest="command",help="可用命令")

    # gateway
    gw_parser=subparsers.add_parser("gateway",help="Gateway服务管理")
    gw_sub=gw_parser.add_subparsers(dest="gw_action")
    gw_sub.add_parser("start",help="启动Gateway")
    gw_sub.add_parser("stop",help="停止Gateway")
    gw_sub.add_parser("status",help="查看Gateway状态")

    # agent
    agent_parser=subparsers.add_parser("agent",help="Agent管理")
    agent_sub=agent_parser.add_subparsers(dest="agent_action")
    reg=agent_sub.add_parser("register",help="注册Agent")
    reg.add_argument("--name",required=True,help="Agent名称")
    reg.add_argument("--type",required=True,choices=["claude","openai","google","nous","custom"],help="Agent类型")
    reg.add_argument("--priority",type=int,default=99,help="优先级")
    agent_sub.add_parser("list",help="列出所有Agent")
    agent_sub.add_parser("stats",help="Agent统计")

    # skill
    skill_parser=subparsers.add_parser("skill",help="技能管理")
    skill_sub=skill_parser.add_subparsers(dest="skill_action")
    inst=skill_sub.add_parser("install",help="安装技能")
    inst.add_argument("--name",required=True,help="技能名称")
    skill_sub.add_parser("list",help="列出所有技能")
    skill_sub.add_parser("stats",help="技能统计")

    # quality
    quality_parser=subparsers.add_parser("quality",help="品质检测")
    quality_sub=quality_parser.add_subparsers(dest="quality_action")
    check=quality_sub.add_parser("check",help="检测文本品质")
    check.add_argument("--file",help="文本文件路径")
    check.add_argument("--text",help="直接输入文本")

    # cost
    cost_parser=subparsers.add_parser("cost",help="成本管理")
    cost_sub=cost_parser.add_subparsers(dest="cost_action")
    cost_sub.add_parser("status",help="查看预算状态")
    cost_sub.add_parser("report",help="生成用量报告")

    # sync
    sync_parser=subparsers.add_parser("sync",help="内容同步")
    sync_sub=sync_parser.add_subparsers(dest="sync_action")
    sync_sub.add_parser("platforms",help="列出支持的平台")
    pub=sync_sub.add_parser("publish",help="发布内容")
    pub.add_argument("--title",required=True,help="标题")
    pub.add_argument("--body",required=True,help="正文")
    pub.add_argument("--platforms",nargs="+",default=["devto"],help="目标平台")

    # run
    run_parser=subparsers.add_parser("run",help="执行任务")
    run_parser.add_argument("task",nargs="+",help="任务描述")

    args=parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    print(f"AetherFlow v0.1.0 - {args.command}")

    if args.command=="gateway":
        from src.core.gateway import AetherFlowGateway
        gw=AetherFlowGateway()
        if args.gw_action=="start":
            asyncio.run(gw.start())
        elif args.gw_action=="status":
            print(gw.get_status())

    elif args.command=="agent":
        from src.agents.registry import AgentRegistry,AgentInfo,AgentType,AgentCapability
        registry=AgentRegistry()
        if args.agent_action=="register":
            info=AgentInfo(
                name=args.name,
                agent_type=AgentType(args.type),
                priority=args.priority,
                capabilities=AgentCapability(),
            )
            registry.register(info)
        elif args.agent_action=="list":
            agents=registry.list_agents()
            if agents:
                for a in agents:
                    print(f"  [{a.priority}] {a.name} ({a.agent_type.value}) - {a.status.value}")
            else:
                print("  暂无注册Agent")
        elif args.agent_action=="stats":
            stats=registry.get_stats()
            print(f"  Agent总数: {stats['total_agents']}")
            print(f"  在线: {stats['online']}  |  忙碌: {stats['busy']}")

    elif args.command=="skill":
        from src.skills.manager import SkillManager
        manager=SkillManager(Path("skills_builtin"))
        if args.skill_action=="list":
            skills=manager.list_skills()
            if skills:
                for s in skills:
                    print(f"  [{s.metadata.category.value}] {s.metadata.name} v{s.metadata.version}")
            else:
                print("  暂无安装技能")
        elif args.skill_action=="stats":
            stats=manager.get_stats()
            print(f"  技能总数: {stats['total_skills']}")
            print(f"  启用: {stats['enabled']}  |  禁用: {stats['disabled']}")

    elif args.command=="quality":
        from src.quality_engine.anti_homogenizer import AntiHomogenizer
        engine=AntiHomogenizer()
        if args.quality_action=="check":
            if args.file:
                text=Path(args.file).read_text(encoding="utf-8")
            elif args.text:
                text=args.text
            else:
                print("请指定 --file 或 --text")
                return
            report=engine.analyze(text)
            print(f"  品质评分: {report.overall_score}/100 [{report.level.value}]")
            print(f"  短语层面: {report.phrase_score} | 结构层面: {report.structure_score} | 语义层面: {report.semantic_score}")
            if report.suggestions:
                print("  建议:")
                for s in report.suggestions:
                    print(f"    - {s}")

    elif args.command=="cost":
        from src.cost_optimizer.smart_router import SmartCostRouter
        router=SmartCostRouter()
        if args.cost_action=="status":
            status=router.get_budget_status()
            print(f"  月预算: ${status['monthly_budget']}")
            print(f"  已使用: ${status['current_spend']} ({status['percent_used']}%)")
            print(f"  状态: {status['status']}")
        elif args.cost_action=="report":
            report=router.get_usage_report()
            print(f"  总调用: {report['total_calls']}")
            print(f"  总花费: ${report['total_cost']}")

    elif args.command=="sync":
        from src.content_sync.sync_engine import ContentSyncEngine
        engine=ContentSyncEngine()
        if args.sync_action=="platforms":
            platforms=engine.get_supported_platforms()
            print(f"  支持 {len(platforms)} 个平台:")
            for p in platforms:
                print(f"    [{p['type']}] {p['name']} ({p['id']})")

    elif args.command=="run":
        task=" ".join(args.task)
        print(f"  执行任务: {task}")
        print("  [任务已提交到编排器，等待Agent执行...]")

if __name__=="__main__":
    main()
