"""
测试 - 品质引擎
"""
import pytest
from src.quality_engine.anti_homogenizer import AntiHomogenizer,QualityLevel

def test_analyze_original_text():
    engine=AntiHomogenizer()
    text="昨天下了一场好大的雨，窗外的梧桐树被打得沙沙作响。我泡了一杯茶，翻开那本读了一半的小说。"
    report=engine.analyze(text,lang="zh")
    assert report.overall_score>=60
    assert report.level in [QualityLevel.GOOD,QualityLevel.EXCELLENT,QualityLevel.FAIR]

def test_analyze_homogenized_text():
    engine=AntiHomogenizer()
    text="在当今数字化时代，赋能企业数字化转型至关重要。众所周知，深入探讨这一议题具有重大意义。总而言之，不可否认的是..."
    report=engine.analyze(text,lang="zh")
    assert report.overall_score<60
    assert len(report.detected_patterns)>0

def test_analyze_english():
    engine=AntiHomogenizer()
    text="In today's digital age, it is worth noting that AI can revolutionize the industry. Furthermore, this paradigm shift is unprecedented."
    report=engine.analyze(text,lang="en")
    assert report.overall_score<60
    assert len(report.detected_patterns)>0

def test_enhance():
    engine=AntiHomogenizer()
    text="在当今时代，赋能企业转型是关键。"
    enhanced=engine.enhance(text,lang="zh")
    assert "赋能" not in enhanced or "在当今时代" not in enhanced

def test_empty_text():
    engine=AntiHomogenizer()
    report=engine.analyze("")
    assert report.overall_score==100.0
