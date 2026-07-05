# 贡献指南 / Contributing Guide

感谢你对AetherFlow的关注！以下指南将帮助你快速上手贡献。

## 快速开始

1. Fork本仓库
2. 克隆到本地: `git clone https://github.com/YOUR_USERNAME/aetherflow.git`
3. 安装依赖: `pip install -e ".[dev]"`
4. 创建分支: `git checkout -b feature/your-feature`
5. 提交PR

## 开发规范

### 代码风格

- Python 3.10+，使用Type Hints
- 遵循PEP 8（行长度120字符）
- 使用 `ruff` 进行代码检查: `ruff check src/`
- 使用 `black` 格式化: `black src/`

### 提交规范

使用约定式提交格式（Conventional Commits）:

```
<type>(<scope>): <description>

- feat: 新功能
- fix: 修复
- docs: 文档
- refactor: 重构
- test: 测试
- chore: 构建/工具
```

示例:
```
feat(skills): 添加code-review技能
fix(orchestrator): 修复并行任务依赖图死锁问题
docs(readme): 更新安装指南
```

### 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定模块测试
pytest tests/test_gateway.py -v

# 生成覆盖率报告
pytest --cov=src tests/ --cov-report=html
```

### 添加新技能

1. 在 `skills_builtin/` 下创建新目录
2. 编写 `SKILL.md`（技能描述和指令）和 `skill.json`（元数据）
3. 在 `tests/test_skills.py` 中添加测试
4. 更新 `README.md` 中的技能表

### 添加新Agent类型

1. 在 `src/agents/registry.py` 中注册新类型
2. 在 `src/core/config.py` 中添加默认配置
3. 更新 `docs/ARCHITECTURE.md`

## 分支策略

- `main`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `fix/*`: 修复分支

## 发布流程

1. 在 `develop` 分支完成开发和测试
2. 更新 `pyproject.toml` 中的版本号
3. 更新 `CHANGELOG.md`
4. 创建版本标签: `git tag -a v0.x.x -m "Release v0.x.x"`
5. 合并到 `main` 并推送标签

## 行为准则

请参阅 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## Quick Start (English)

1. Fork the repository
2. Clone: `git clone https://github.com/YOUR_USERNAME/aetherflow.git`
3. Install: `pip install -e ".[dev]"`
4. Branch: `git checkout -b feature/your-feature`
5. Submit PR

## Development Standards

### Code Style

- Python 3.10+ with Type Hints
- PEP 8 (120 char line length)
- Lint with `ruff`: `ruff check src/`
- Format with `black`: `black src/`

### Commit Convention

Follow Conventional Commits format.

### Testing

```bash
pytest tests/ -v
pytest --cov=src tests/ --cov-report=html
```

### Adding New Skills

Create directory under `skills_builtin/` with `SKILL.md` and `skill.json`.

### Branch Strategy

- `main`: stable
- `develop`: integration
- `feature/*`: features
- `fix/*`: bug fixes

## Release Process

1. Complete dev & testing on `develop`
2. Bump version in `pyproject.toml`
3. Update `CHANGELOG.md`
4. Tag: `git tag -a v0.x.x -m "Release v0.x.x"`
5. Merge to `main` and push tags
