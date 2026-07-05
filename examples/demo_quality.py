"""
示例2：品质检测与增强
演示反同质化引擎的使用
"""
from src.quality_engine.anti_homogenizer import AntiHomogenizer,QualityLevel

def main():
    engine=AntiHomogenizer(originality_threshold=0.6)

    # 测试文本1：原创内容
    original_text="""昨天下了一场大雨，窗外的梧桐树被打得沙沙作响。
    我泡了一壶铁观音，从书架上取下那本已泛黄的《百年孤独》。
    读着读着，雨声渐渐小了，天色也暗了下来。"""

    print("="*60)
    print("测试1：原创文学内容")
    print("="*60)
    report1=engine.analyze(original_text,lang="zh")
    print(f"品质评分: {report1.overall_score}/100 [{report1.level.value}]")
    print(f"短语: {report1.phrase_score} | 结构: {report1.structure_score} | 语义: {report1.semantic_score}")

    # 测试文本2：AI同质化内容
    ai_text="""在当今数字化时代，企业赋能已成为推动经济增长的关键抓手。
    深入探讨这一议题，我们不难发现，数字化转型的落地需要各环节的闭环对齐。
    总而言之，不可否认的是，技术创新正在重塑整个行业生态。
    毫无疑问，这将对未来发展产生深远影响。"""

    print("\n"+"="*60)
    print("测试2：AI同质化内容")
    print("="*60)
    report2=engine.analyze(ai_text,lang="zh")
    print(f"品质评分: {report2.overall_score}/100 [{report2.level.value}]")
    print(f"检测到模式: {len(report2.detected_patterns)}")
    for p in report2.detected_patterns:
        print(f"  - {p['type']}: {p.get('word',p.get('pattern','unknown'))}")
    if report2.suggestions:
        print("\n改进建议:")
        for s in report2.suggestions:
            print(f"  - {s}")

    # 测试文本3：增强后的内容
    print("\n"+"="*60)
    print("测试3：自动增强")
    print("="*60)
    if report2.enhanced_text:
        print("增强前:", ai_text[:100]+"...")
        print("增强后:", report2.enhanced_text[:100]+"...")

    # 测试文本4：英文
    english_text="""In today's digital age, it is worth noting that AI can revolutionize
    the industry. Furthermore, this unprecedented paradigm shift represents a game-changer
    for businesses worldwide. In conclusion, leveraging cutting-edge technology is crucial."""

    print("\n"+"="*60)
    print("测试4：英文同质化内容")
    print("="*60)
    report3=engine.analyze(english_text,lang="en")
    print(f"Quality Score: {report3.overall_score}/100 [{report3.level.value}]")
    print(f"Detected Patterns: {len(report3.detected_patterns)}")

if __name__=="__main__":
    main()
