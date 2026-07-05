"""
智能成本优化器 - AI模型路由与Token管理

借鉴ECC的优化策略（懒加载+上下文压缩+记忆缓存+安全沙箱），
扩展为完整的成本路由系统：
- 实时多模型比价
- 任务特征分析+智能匹配
- 自动降级策略
- Token消耗预测
- 月度预算管理
"""
import time
import logging
from dataclasses import dataclass,field
from typing import Optional
from enum import Enum

logger=logging.getLogger(__name__)

class ModelTier(Enum):
    PREMIUM="premium"      # Claude Opus, GPT-4o
    STANDARD="standard"    # Claude Sonnet, GPT-4o-mini
    BUDGET="budget"        # Claude Haiku, Gemini Flash
    LOCAL="local"          # Ollama, LM Studio

@dataclass
class ModelPricing:
    """模型定价信息（USD/1M tokens）"""
    model_name:str
    tier:ModelTier
    input_price:float
    output_price:float
    context_window:int
    provider:str

# 2026年6月实时定价表
REALTIME_PRICING={
    "claude-opus-4":ModelPricing("claude-opus-4",ModelTier.PREMIUM,15.0,75.0,200000,"anthropic"),
    "claude-sonnet-4":ModelPricing("claude-sonnet-4",ModelTier.STANDARD,3.0,15.0,200000,"anthropic"),
    "claude-haiku-3.5":ModelPricing("claude-haiku-3.5",ModelTier.BUDGET,0.8,4.0,200000,"anthropic"),
    "gpt-4o":ModelPricing("gpt-4o",ModelTier.PREMIUM,5.0,15.0,128000,"openai"),
    "gpt-4o-mini":ModelPricing("gpt-4o-mini",ModelTier.STANDARD,0.15,0.6,128000,"openai"),
    "gemini-2.5-pro":ModelPricing("gemini-2.5-pro",ModelTier.PREMIUM,3.5,10.5,2000000,"google"),
    "gemini-2.5-flash":ModelPricing("gemini-2.5-flash",ModelTier.BUDGET,0.15,0.6,1000000,"google"),
    "deepseek-v3":ModelPricing("deepseek-v3",ModelTier.STANDARD,0.27,1.1,128000,"deepseek"),
}

@dataclass
class CostEstimate:
    """成本估算"""
    model:str
    estimated_input_tokens:int
    estimated_output_tokens:int
    estimated_cost:float
    confidence:float  # 0-1

@dataclass
class BudgetTracker:
    """预算追踪"""
    monthly_budget:float=500.0
    current_spend:float=0.0
    month_start:float=0.0
    daily_limits:dict=field(default_factory=dict)

class SmartCostRouter:
    """智能成本路由——选择最优性价比模型"""

    def __init__(self,budget_monthly:float=500.0,auto_downgrade:bool=True,cache_enabled:bool=True):
        self.pricing=REALTIME_PRICING
        self.budget_tracker=BudgetTracker(monthly_budget=budget_monthly)
        self.auto_downgrade=auto_downgrade
        self.cache_enabled=cache_enabled
        self._response_cache={}
        self._usage_history=[]

    def select_model(self,task:dict,quality_requirement:str="standard")->str:
        """智能选择最优模型"""
        candidates=self._filter_candidates(task,quality_requirement)

        if not candidates:
            return "claude-sonnet-4"  # 默认安全选择

        task_tokens=self._estimate_task_tokens(task)
        budget_factor=self._calculate_budget_factor()

        scored=[]
        for model_name,pricing in candidates.items():
            cost_score=self._calculate_cost_score(pricing,task_tokens)
            quality_score=self._calculate_quality_score(pricing,task)
            speed_score=self._calculate_speed_score(pricing,task)

            final_score=(cost_score*0.4+quality_score*0.4+speed_score*0.2)*budget_factor
            scored.append((final_score,model_name))

        scored.sort(key=lambda x:x[0],reverse=True)
        best_model=scored[0][1]

        logger.info(f"智能路由选择: {best_model} (分数: {scored[0][0]:.2f})")
        return best_model

    def estimate_cost(self,model:str,input_tokens:int,output_tokens:int)->CostEstimate:
        """估算成本"""
        pricing=self.pricing.get(model)
        if not pricing:
            pricing=self.pricing["claude-sonnet-4"]

        cost=(input_tokens/1_000_000)*pricing.input_price+(output_tokens/1_000_000)*pricing.output_price
        return CostEstimate(
            model=model,
            estimated_input_tokens=input_tokens,
            estimated_output_tokens=output_tokens,
            estimated_cost=round(cost,4),
            confidence=0.8,
        )

    def record_usage(self,model:str,input_tokens:int,output_tokens:int):
        """记录实际使用量"""
        cost_est=self.estimate_cost(model,input_tokens,output_tokens)
        self.budget_tracker.current_spend+=cost_est.estimated_cost
        self._usage_history.append({
            "timestamp":time.time(),
            "model":model,
            "input_tokens":input_tokens,
            "output_tokens":output_tokens,
            "cost":cost_est.estimated_cost,
        })
        logger.debug(f"用量记录: {model} {input_tokens}+{output_tokens} tokens, ${cost_est.estimated_cost:.4f}")

    def get_budget_status(self)->dict:
        """获取预算状态"""
        bt=self.budget_tracker
        remaining=bt.monthly_budget-bt.current_spend
        percent_used=(bt.current_spend/bt.monthly_budget*100) if bt.monthly_budget>0 else 0
        return {
            "monthly_budget":bt.monthly_budget,
            "current_spend":round(bt.current_spend,2),
            "remaining":round(remaining,2),
            "percent_used":round(percent_used,1),
            "status":"warning" if percent_used>80 else "normal" if percent_used<60 else "caution",
            "projected_monthly":round(bt.current_spend/max(1,time.time()-bt.month_start)*30*86400,2) if bt.month_start else 0,
        }

    def get_cache_key(self,task:dict)->str:
        """生成缓存键"""
        import hashlib
        import json
        content=json.dumps(task,sort_keys=True,default=str)
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def get_cached_response(self,cache_key:str)->Optional[str]:
        """获取缓存响应"""
        if not self.cache_enabled:
            return None
        entry=self._response_cache.get(cache_key)
        if entry and time.time()-entry["timestamp"]<3600:
            return entry["response"]
        return None

    def set_cached_response(self,cache_key:str,response:str):
        """设置缓存响应"""
        if self.cache_enabled:
            self._response_cache[cache_key]={"response":response,"timestamp":time.time()}

    def _filter_candidates(self,task:dict,quality:str)->dict:
        """过滤候选模型"""
        task_complexity=task.get("complexity","medium")
        candidates={}

        for name,pricing in self.pricing.items():
            if quality=="premium" and pricing.tier==ModelTier.BUDGET:
                continue
            if quality=="fast" and pricing.tier==ModelTier.PREMIUM:
                continue
            candidates[name]=pricing

        if not candidates:
            candidates["claude-sonnet-4"]=self.pricing["claude-sonnet-4"]

        return candidates

    def _estimate_task_tokens(self,task:dict)->dict:
        """估算任务Token消耗"""
        description_len=len(task.get("description",""))
        return {
            "input":max(500,description_len*2),
            "output":max(200,description_len),
        }

    def _calculate_budget_factor(self)->float:
        """计算预算因子"""
        status=self.get_budget_status()
        if status["percent_used"]>90:
            return 0.3  # 极度节省
        elif status["percent_used"]>75:
            return 0.6
        elif status["percent_used"]>50:
            return 0.8
        return 1.0

    def _calculate_cost_score(self,pricing:ModelPricing,tokens:dict)->float:
        """计算成本分数"""
        total_cost=(tokens["input"]/1_000_000)*pricing.input_price+(tokens["output"]/1_000_000)*pricing.output_price
        max_cost=0.1
        return max(0,min(1,1-total_cost/max_cost))

    def _calculate_quality_score(self,pricing:ModelPricing,task:dict)->float:
        """计算质量分数"""
        tier_scores={ModelTier.PREMIUM:1.0,ModelTier.STANDARD:0.8,ModelTier.BUDGET:0.5,ModelTier.LOCAL:0.3}
        return tier_scores.get(pricing.tier,0.5)

    def _calculate_speed_score(self,pricing:ModelPricing,task:dict)->float:
        """计算速度分数"""
        tier_scores={ModelTier.BUDGET:1.0,ModelTier.STANDARD:0.8,ModelTier.PREMIUM:0.5,ModelTier.LOCAL:0.7}
        return tier_scores.get(pricing.tier,0.7)

    def get_usage_report(self)->dict:
        """生成用量报告"""
        if not self._usage_history:
            return {"total_calls":0,"total_cost":0.0,"by_model":{}}

        by_model={}
        for entry in self._usage_history:
            model=entry["model"]
            if model not in by_model:
                by_model[model]={"calls":0,"total_cost":0,"total_tokens":0}
            by_model[model]["calls"]+=1
            by_model[model]["total_cost"]+=entry["cost"]
            by_model[model]["total_tokens"]+=entry["input_tokens"]+entry["output_tokens"]

        return {
            "total_calls":len(self._usage_history),
            "total_cost":round(sum(e["cost"] for e in self._usage_history),4),
            "total_tokens":sum(e["input_tokens"]+e["output_tokens"] for e in self._usage_history),
            "by_model":by_model,
            "cache_hits":len(self._response_cache),
        }
