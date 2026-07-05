# 更新日志 / Changelog

## [0.1.0] - 2026-06-06

### Added

#### 核心架构
- Gateway统一入口：WebSocket/HTTP双协议接入
- Agent注册中心：支持Claude/Codex/Gemini/Hermes多模型注册
- 技能管理器：SKILL.md标准格式，全生命周期管理
- 智能编排器：多Agent并行Swarm协作，依赖图调度

#### 品质引擎
- 反同质化引擎：短语/结构/语义三级检测
- AI高频用语词库：中英文共50+词汇
- 模板化结构检测
- 自动品质增强

#### 成本优化
- 智能模型路由：实时多模型比价
- Token消耗预测
- 月预算管理
- 响应缓存

#### 数据层
- 统一数据层：SQLite+向量+知识图谱
- 文档存储与检索
- 会话记忆管理
- 知识图谱三元组

#### 内容同步
- 20+平台内容分发
- 自适应格式转换
- MCP Server模式支持

#### 内置技能
- code-review: 代码审查
- blog-writer: 博客生成
- doc-translator: 文档翻译
- api-builder: API构建
- data-analyzer: 数据分析
- shell-master: Shell自动化
- rag-assistant: RAG知识库

### Documentation
- 中文README：完整使用指南
- 英文README_EN：English User Guide
- ARCHITECTURE.md：5W1H架构设计文档
- CONTRIBUTING.md：贡献指南（中英双语）
- CHANGELOG.md：本文件
