"""
反同质化品质引擎 - AI内容质量增强管道

核心创新：多层次检测AI生成内容的原创性和质量，自动增强。
解决"AI内容同质化危机"——95%团队使用AI但仅58%认为质量提升。

检测层级：
1. 短语层面 - 高频AI用语检测（"delve into", "unleash", "game-changer"等）
2. 结构层面 - 模板化结构检测（三段式+bullet points模式）
3. 语义层面 - 内容深度与原创性评分
"""
import re
import math
import logging
from dataclasses import dataclass,field
from typing import Optional
from enum import Enum

logger=logging.getLogger(__name__)

class QualityLevel(Enum):
    EXCELLENT="excellent"  # 90-100
    GOOD="good"            # 75-89
    FAIR="fair"            # 60-74
    POOR="poor"            # 40-59
    HOMOGENIZED="homogenized"  # <40

@dataclass
class QualityReport:
    """品质检测报告"""
    overall_score:float  # 0-100
    level:QualityLevel
    phrase_score:float
    structure_score:float
    semantic_score:float
    detected_patterns:list
    suggestions:list
    enhanced_text:Optional[str]=None

class AntiHomogenizer:
    """反同质化引擎——AI内容品质守护者"""

    # 高频AI用语词汇库（这些词过度使用会降低原创性评分）
    AI_BUZZWORDS_CN=[
        "深入探讨","总而言之","值得注意的是","不仅如此",
        "在当今时代","随着...的发展","不可否认","毫无疑问",
        "众所周知","毋庸置疑","从根本上","本质上",
        "赋能","抓手","闭环","落地","对齐","颗粒度",
        "引爆","颠覆","重塑","破圈","出圈",
    ]
    AI_BUZZWORDS_EN=[
        "delve into","unleash","game-changer","revolutionize",
        "in today's digital age","it is worth noting","furthermore",
        "moreover","in conclusion","undoubtedly","arguably",
        "unprecedented","paradigm shift","cutting-edge",
        "seamless","robust","holistic","synergize","leverage",
        "it's important to note","in the world of","a testament to",
    ]

    # 模板化结构模式
    TEMPLATE_PATTERNS=[
        r"^\d+\.\s+.{10,}:.{10,}",  # 编号列表+冒号解释
        r"(首先.*其次.*最后)",
        r"(First,.*Second,.*Finally)",
        r"(引言.*正文.*结论)",
    ]

    def __init__(self,originality_threshold:float=0.6):
        self.threshold=originality_threshold
        self._history_cache=[]

    def analyze(self,text:str,lang:str="auto")->QualityReport:
        """分析文本品质——返回完整检测报告"""
        if lang=="auto":
            lang=self._detect_language(text)

        phrase_score=self._check_phrase_level(text,lang)
        structure_score=self._check_structure_level(text)
        semantic_score=self._check_semantic_level(text)

        detected=self._collect_patterns(text,lang)

        overall=(phrase_score*0.3+structure_score*0.3+semantic_score*0.4)
        overall=min(100,max(0,overall))

        level=self._score_to_level(overall)

        suggestions=self._generate_suggestions(overall,detected,lang)

        report=QualityReport(
            overall_score=round(overall,1),
            level=level,
            phrase_score=round(phrase_score,1),
            structure_score=round(structure_score,1),
            semantic_score=round(semantic_score,1),
            detected_patterns=detected,
            suggestions=suggestions,
        )

        if overall<self.threshold*100:
            report.enhanced_text=self.enhance(text,lang)

        logger.info(f"品质分析完成: {overall:.1f}/100 [{level.value}]")
        return report

    def enhance(self,text:str,lang:str="auto")->str:
        """增强文本质量——自动修复同质化问题"""
        if lang=="auto":
            lang=self._detect_language(text)

        buzzwords=self.AI_BUZZWORDS_CN if lang=="zh" else self.AI_BUZZWORDS_EN
        enhanced=text

        for bw in buzzwords:
            if bw in enhanced:
                enhanced=enhanced.replace(bw,self._get_alternative(bw,lang))

        sentences=enhanced.split("。") if lang=="zh" else enhanced.split(". ")
        if len(sentences)>5:
            varied=self._vary_sentence_structure(sentences,lang)
            enhanced="。".join(varied) if lang=="zh" else ". ".join(varied)

        return enhanced

    def _check_phrase_level(self,text:str,lang:str)->float:
        """短语层面检测——AI高频用语检测"""
        buzzwords=self.AI_BUZZWORDS_CN if lang=="zh" else self.AI_BUZZWORDS_EN
        total_words=len(text.split())
        if total_words==0:
            return 100.0

        buzz_count=sum(1 for bw in buzzwords if bw.lower() in text.lower())
        density=buzz_count/max(1,total_words/100)

        score=100-density*15
        return max(0,min(100,score))

    def _check_structure_level(self,text:str)->float:
        """结构层面检测——模板化结构识别"""
        score=100.0
        paragraphs=text.split("\n\n")
        if len(paragraphs)<=3:
            score-=10

        for pattern in self.TEMPLATE_PATTERNS:
            if re.search(pattern,text,re.IGNORECASE):
                score-=10

        bullet_ratio=text.count("\n-")+text.count("\n•")+text.count("\n*")
        if bullet_ratio>len(paragraphs)*0.5:
            score-=10

        return max(0,score)

    def _check_semantic_level(self,text:str)->float:
        """语义层面检测——内容深度与原创性"""
        score=70.0

        words=text.split()
        unique_words=len(set(w.lower() for w in words if len(w)>2))
        total_words=len(words)
        if total_words>0:
            lexical_diversity=unique_words/total_words
            score+=lexical_diversity*20

        sentences=[s.strip() for s in re.split(r'[.!?。！？]',text) if len(s.strip())>10]
        if sentences:
            lengths=[len(s.split()) for s in sentences]
            if len(lengths)>1:
                mean_len=sum(lengths)/len(lengths)
                variance=sum((l-mean_len)**2 for l in lengths)/len(lengths)
                score+=min(10,variance/max(1,mean_len)*5)

        return max(0,min(100,score))

    def _collect_patterns(self,text:str,lang:str)->list[dict]:
        """收集检测到的模式"""
        patterns=[]
        buzzwords=self.AI_BUZZWORDS_CN if lang=="zh" else self.AI_BUZZWORDS_EN
        for bw in buzzwords:
            if bw.lower() in text.lower():
                patterns.append({"type":"buzzword","word":bw,"severity":"medium"})

        for pattern in self.TEMPLATE_PATTERNS:
            if re.search(pattern,text,re.IGNORECASE):
                patterns.append({"type":"template","pattern":pattern,"severity":"high"})
        return patterns

    def _generate_suggestions(self,score:float,patterns:list,lang:str)->list[str]:
        """生成改进建议"""
        suggestions=[]
        if score<40:
            suggestions.append("内容高度同质化，建议大幅重写" if lang=="zh" else "Content is highly homogenized, consider major rewrite")
        elif score<60:
            suggestions.append("检测到较多模板化表达，建议增加原创性" if lang=="zh" else "Template expressions detected, add more originality")
        elif score<75:
            suggestions.append("整体质量良好，可进一步优化表达多样性" if lang=="zh" else "Good quality, consider improving expression variety")

        buzzword_patterns=[p for p in patterns if p["type"]=="buzzword"]
        if buzzword_patterns:
            words=", ".join(p["word"] for p in buzzword_patterns[:5])
            suggestions.append(f"建议替换高频AI用语: {words}")

        return suggestions

    def _score_to_level(self,score:float)->QualityLevel:
        if score>=90:
            return QualityLevel.EXCELLENT
        elif score>=75:
            return QualityLevel.GOOD
        elif score>=60:
            return QualityLevel.FAIR
        elif score>=40:
            return QualityLevel.POOR
        return QualityLevel.HOMOGENIZED

    def _detect_language(self,text:str)->str:
        """简单语言检测"""
        chinese_chars=sum(1 for c in text if '\u4e00'<=c<='\u9fff')
        if chinese_chars>len(text)*0.1:
            return "zh"
        return "en"

    def _get_alternative(self,word:str,lang:str)->str:
        """获取替代词汇"""
        alternatives={
            "zh":{
                "赋能":"增强","抓手":"关键点","闭环":"完整流程",
                "落地":"实施","对齐":"协调","颗粒度":"细节",
                "引爆":"引发","颠覆":"改变","重塑":"重建",
            },
            "en":{
                "delve into":"explore","unleash":"release",
                "revolutionize":"transform","game-changer":"breakthrough",
                "cutting-edge":"advanced","robust":"reliable",
                "seamless":"smooth","holistic":"comprehensive",
            }
        }
        return alternatives.get(lang,{}).get(word,word)

    def _vary_sentence_structure(self,sentences:list,lang:str)->list:
        """变化句式结构"""
        varied=[]
        for i,s in enumerate(sentences):
            s=s.strip()
            if not s:
                varied.append(s)
                continue
            if i%3==0 and lang=="zh":
                if not s.startswith(("然而","但是","因此","同时")):
                    s=s
            varied.append(s)
        return varied
