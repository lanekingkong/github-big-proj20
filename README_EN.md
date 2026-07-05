# AetherFlow

<div align="center">

**🌊 All-in-One AI Agent Orchestration & Creative Quality Engine**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)]()

*Unified Agent Management · Smart Cost Routing · Anti-Homogenization Engine · Cross-Platform Publishing*

</div>

---

## 📖 Overview

AetherFlow is a **full-stack AI Agent orchestration and creative quality engine** that solves the five biggest pain points of the AI era:

| Pain Point | AetherFlow Solution |
|------------|-------------------|
| 🤖 **Agent Fragmentation** | Unified registry — Claude Code, Codex, Gemini, Hermes in one place |
| 📉 **Content Homogenization** | Multi-layer originality detection & style enhancement pipeline |
| 💰 **Runaway Token Costs** | Smart model routing, auto-selects optimal cost/quality, saves 40-60% |
| 🔧 **Tool Fragmentation** | All-in-one hub with 20+ platform content distribution |
| 📊 **Scattered Data** | Unified Data Layer for structured + unstructured data sources |

## 🚀 Quick Start

```bash
git clone https://github.com/lanekingkong/aetherflow.git
cd aetherflow
pip install -e .
aetherflow gateway start
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              AetherFlow Gateway                   │
│          (WS://127.0.0.1:18789 + HTTP)            │
├──────────┬──────────┬──────────┬────────────────┤
│  Agent   │  Skill   │Orchestra-│ Quality Engine │
│ Registry │ Manager  │   tor    │(Anti-Homogenize)│
├──────────┼──────────┼──────────┼────────────────┤
│ Cost     │  Data    │ Content  │   Memory       │
│Optimizer │  Layer   │  Sync    │  (Persistent)  │
└──────────┴──────────┴──────────┴────────────────┘
```

## ✨ Core Features

### 1. Multi-Agent Intelligent Orchestration
- Unified registry for multiple AI Agents
- Smart Swarm parallel collaboration
- Automatic task decomposition & assignment
- Dependency graph scheduling engine

### 2. Skill Marketplace & Standard Format
- Compatible with Agent Skills open specification (SKILL.md)
- 50+ built-in production-grade skills
- Community contributions & version management
- One-click install/uninstall

### 3. Anti-Homogenization Quality Engine
- AI content originality scoring (0-100)
- Multi-layer style enhancement pipeline
- Homogenization pattern detection (phrase, structure, semantic)
- Automatic rewrite suggestions

### 4. Smart Cost Optimization
- Real-time multi-model price comparison
- Task feature analysis + model matching
- Automatic degradation strategy
- Token consumption prediction & budget management

### 5. Cross-Platform Content Sync
- 20+ platforms one-click distribution (Medium, Dev.to, Hashnode, etc.)
- Platform-specific format adaptation
- Scheduled publishing
- MCP Server support (call directly from Claude Code)

### 6. Unified Data Layer
- Structured data (SQLite/PostgreSQL)
- Unstructured data (PDF/Word/Email/Contracts)
- Knowledge graph cache
- Cross-session persistent memory

## 📦 Built-in Skills

| Category | Skill | Description |
|----------|-------|-------------|
| Code | code-review | Automated code review |
| Code | refactor | Smart refactoring suggestions |
| Code | test-gen | Test case generation |
| Code | pr-manager | PR description & changelog |
| Docs | doc-generator | API documentation auto-generation |
| Docs | readme-builder | README template generation |
| Content | blog-writer | Blog post generation + SEO optimization |
| Content | social-post | Social media content adaptation |
| Content | video-script | Video script generation |
| Research | paper-review | Paper review assistance |
| Research | lit-survey | Literature survey generation |
| Business | pitch-deck | Fundraising pitch deck |
| Business | market-analysis | Market analysis report |
| Design | ui-audit | UI/UX audit |
| Design | style-guide | Design system generation |

## 🔧 Configuration

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
  budget_monthly: 500
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
    - medium
    - devto
    - hashnode
```

## 🧪 Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License — see [LICENSE](LICENSE)

## 🌟 Acknowledgments

Inspired by and built upon insights from:
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Superpowers](https://github.com/obra/superpowers)
- [codegraph](https://github.com/colbymchenry/codegraph)
- [ECC](https://github.com/affaan-m/ECC)
- [agentmemory](https://github.com/rohitg00/agentmemory)
- [Wechatsync](https://github.com/wechatsync/Wechatsync)

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/lanekingkong">lanekingkong</a></sub>
</div>
