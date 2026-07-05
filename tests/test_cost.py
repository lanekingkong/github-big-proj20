"""
测试 - 成本优化器
"""
import pytest
from src.cost_optimizer.smart_router import SmartCostRouter,ModelTier

def test_select_model_basic():
    router=SmartCostRouter(budget_monthly=500.0)
    task={"description":"简单问答","complexity":"low","category":"qa"}
    model=router.select_model(task,quality_requirement="standard")
    assert model in router.pricing

def test_select_model_premium():
    router=SmartCostRouter(budget_monthly=1000.0)
    task={"description":"复杂代码架构分析","complexity":"high","category":"code"}
    model=router.select_model(task,quality_requirement="premium")
    assert model in router.pricing

def test_estimate_cost():
    router=SmartCostRouter()
    est=router.estimate_cost("claude-sonnet-4",10000,1000)
    assert est.estimated_cost>0
    assert est.model=="claude-sonnet-4"

def test_record_usage():
    router=SmartCostRouter()
    router.record_usage("claude-sonnet-4",5000,500)
    status=router.get_budget_status()
    assert status["current_spend"]>0

def test_budget_status():
    router=SmartCostRouter(budget_monthly=100.0)
    status=router.get_budget_status()
    assert status["monthly_budget"]==100.0
    assert status["remaining"]==100.0
    assert status["status"]=="normal"

def test_cache():
    router=SmartCostRouter(cache_enabled=True)
    task={"query":"test cache"}
    key=router.get_cache_key(task)
    assert key is not None
    assert router.get_cached_response(key) is None
    router.set_cached_response(key,"test response")
    assert router.get_cached_response(key)=="test response"
