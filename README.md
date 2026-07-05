# AetherFlow

<div align="center">

**🌊 全能AI智能体编排与创作品质引擎**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)]()

*统一多Agent管理 · 智能成本路由 · 反同质化内容增强 · 跨平台分发*

</div>

---

## 📖 简介

AetherFlow 是一个**全栈AI智能体编排与创作品质引擎**，解决AI时代五大核心痛点：

| 痛点 | AetherFlow 解决方案 |
|------|-------------------|
| 🤖 **Agent碎片化** | 统一注册中心，一键切换Claude Code/Codex/Gemini/Hermes |
| 📉 **内容同质化** | 反同质化质量引擎，多层次原创检测与风格增强 |
| 💰 **Token成本失控** | 智能模型路由，自动选择最优性价比，节省40-60%成本 |
| 🔧 **工具碎片化** | 一站式中台，集成20+平台内容分发 |
| 📊 **数据分散** | 统一Data Layer，结构化+非结构化数据无缝接入 |

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/lanekingkong/aetherflow.git
cd aetherflow

# 安装依赖
pip install -e .

# 启动Gateway
aetherflow gateway start

# 注册Agent
aetherflow agent register --name claude-code --type claude

# 加载技能
aetherflow skill install --name code-review

# 执行任务
aetherflow run "帮我审查这个PR并生成发布说明"
```

## 🏗️ 架构

```
┌─────────────────────────────────────────────────┐
│              AetherFlow Gateway                   │
│          (WS://127.0.0.1:18789 + HTTP)            │
├──────────┬──────────┬──────────┬────────────────┤
│  Agent   │  Skill   │Orchestra-│ Quality Engine │
│ Registry │ Manager  │   tor    │ (反同质化引擎)  │
├──────────┼──────────┼──────────┼────────────────┤
│ Cost     │  Data    │ Content  │   Memory       │
│Optimizer │  Layer   │  Sync    │   (持久记忆)   │
└──────────┴──────────┴──────────┴────────────────┘
```

## ✨ 核心特性

### 1. 多Agent智能编排
- 统一注册中心管理多个AI Agent
- 智能Swarm并行协作
- 任务自动拆解与分配
- 依赖图调度引擎

### 2. 技能市场与标准格式
- 兼容Agent Skills开放规范（SKILL.md）
- 50+内置生产级技能
- 社区贡献与版本管理
- 一键安装/卸载

### 3. 反同质化质量引擎
- AI内容原创性评分（0-100）
- 多层次风格增强管道
- 同质化模式检测（短语、结构、语义三层）
- 自动改写建议

### 4. 智能成本优化
- 实时多模型比价
- 任务特征分析+模型匹配
- 自动降级策略
- Token消耗预测与预算管理

### 5. 跨平台内容同步
- 支持20+平台一键分发（微信公众号、知乎、掘金、CSDN、简书、Medium、Dev.to等）
- 平台格式自适应
- 定时排期发布
- MCP Server支持（Claude Code内直接调用）

### 6. 统一数据层
- 结构化数据（SQLite/PostgreSQL）
- 非结构化数据（PDF/Word/邮件/合同）
- 知识图谱缓存
- 跨会话持久记忆

## 📦 内置技能

| 类别 | 技能 | 描述 |
|------|------|------|
| 代码 | code-review | 自动化代码审查 |
| 代码 | refactor | 智能重构建议 |
| 代码 | test-gen | 测试用例生成 |
| 代码 | pr-manager | PR描述与变更日志 |
| 文档 | doc-generator | API文档自动生成 |
| 文档 | readme-builder | README模板生成 |
| 内容 | blog-writer | 博客文章生成+SEO优化 |
| 内容 | social-post | 社交媒体内容适配 |
| 内容 | video-script | 视频脚本生成 |
| 研究 | paper-review | 论文审稿辅助 |
| 研究 | lit-survey | 文献综述生成 |
| 商业 | pitch-deck | 融资演讲稿生成 |
| 商业 | market-analysis | 市场分析报告 |
| 设计 | ui-audit | UI/UX审查 |
| 设计 | style-guide | 设计系统生成 |

## 🔧 配置

```yaml
# aetherflow.yaml
gateway:
  host: 127.0.0.1
  port: 18789

agents:
  claude-code:
    type: claude
    priority: 1
  codex:
    type: openai
    priority: 2
  gemini:
    type: google
    priority: 3

cost_optimizer:
  budget_monthly: 500  # 月预算USD
  auto_downgrade: true
  cache_enabled: true

quality_engine:
  originality_threshold: 0.6
  auto_enhance: true
  style_presets:
    - professional
    - creative
    - academic

content_sync:
  platforms:
    - wechat
    - zhihu
    - juejin
    - medium
    - devto
  schedule:
    enabled: true
    timezone: Asia/Shanghai
```

## 🧪 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定模块测试
pytest tests/test_orchestrator.py -v

# 带覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 🤝 贡献

欢迎贡献！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

### 贡献流程
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 技能贡献
- 技能目录结构：独立文件夹 + SKILL.md
- 参考 `skills_builtin/` 中的示例
- 提交到 `community_skills/` 目录

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE)

## 🌟 致谢

本项目借鉴并致敬以下开源项目：
- [OpenClaw](https://github.com/openclaw/openclaw) - 本地优先AI助手架构
- [Superpowers](https://github.com/obra/superpowers) - Agent Skills标准框架
- [codegraph](https://github.com/colbymchenry/codegraph) - 代码知识图谱
- [ECC](https://github.com/affaan-m/ECC) - Agent性能优化
- [agentmemory](https://github.com/rohitg00/agentmemory) - 持久记忆系统
- [Wechatsync](https://github.com/wechatsync/Wechatsync) - 多平台同步

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/lanekingkong">lanekingkong</a></sub>
</div>
