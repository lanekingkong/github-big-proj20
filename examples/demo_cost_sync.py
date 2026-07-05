"""
示例3：智能成本和内容同步
演示成本路由和内容同步功能
"""
from src.cost_optimizer.smart_router import SmartCostRouter
from src.content_sync.sync_engine import ContentSyncEngine,ContentItem

def demo_cost():
    print("="*60)
    print("智能成本路由演示")
    print("="*60)

    router=SmartCostRouter(budget_monthly=500.0)

    # 不同复杂度任务的路由结果
    tasks=[
        {"description":"简单问答：1+1等于几","complexity":"low","category":"qa"},
        {"description":"代码审查：检查Python项目的安全漏洞","complexity":"medium","category":"code"},
        {"description":"架构设计：设计一个分布式微服务系统的完整架构","complexity":"high","category":"architecture"},
    ]

    for task in tasks:
        model=router.select_model(task)
        est=router.estimate_cost(model,5000,1000)
        print(f"\n  任务: {task['description'][:40]}...")
        print(f"  路由到: {model}")
        print(f"  预估成本: ${est.estimated_cost}")

    # 模拟使用
    router.record_usage("claude-sonnet-4",10000,2000)
    router.record_usage("deepseek-v3",5000,500)
    router.record_usage("gemini-2.5-flash",3000,300)

    status=router.get_budget_status()
    print(f"\n  预算状态:")
    print(f"    月预算: ${status['monthly_budget']}")
    print(f"    已使用: ${status['current_spend']} ({status['percent_used']}%)")
    print(f"    状态: {status['status']}")

    report=router.get_usage_report()
    print(f"\n  用量报告:")
    print(f"    总调用: {report['total_calls']}")
    print(f"    总花费: ${report['total_cost']}")

def demo_sync():
    print("\n"+"="*60)
    print("内容同步引擎演示")
    print("="*60)

    engine=ContentSyncEngine()

    # 列出支持平台
    platforms=engine.get_supported_platforms()
    print(f"\n  支持 {len(platforms)} 个平台:")
    for p in platforms[:6]:
        print(f"    [{p['type']}] {p['name']} ({p['id']})")

    # 创建内容
    content=ContentItem(
        title="AetherFlow：全能AI智能体编排引擎的设计与实现",
        body="""## 引言

AetherFlow是一个开源的AI智能体编排平台，旨在解决当前AI工具碎片化和内容同质化问题。

## 核心特性

- **智能路由**：自动选择最优性价比模型
- **技能市场**：50+内置技能，社区共建
- **反同质化引擎**：AI内容品质守护
- **跨平台同步**：20+平台一键分发

## 架构设计

采用三层架构：Gateway接入层 → Agent编排层 → 基础设施层...
""",
        author="AetherFlow Team",
        tags=["AI","agent","orchestration","open-source"],
    )

    # 预览发布计划
    target=["devto","medium","zhihu","juejin"]
    plan=engine.preview_publish_plan(content,target)
    print(f"\n  发布计划 (目标: {', '.join(target)}):")
    for plat,detail in plan.items():
        print(f"    [{plat}] {detail['title'][:30]}... ({detail['body_length']}字符)")

    # MCP Schema
    schema=engine.generate_mcp_tool_schema()
    print(f"\n  MCP工具Schema: {schema['name']}")
    print(f"    参数数量: {len(schema['inputSchema']['properties'])}")

if __name__=="__main__":
    demo_cost()
    demo_sync()
