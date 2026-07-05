# code-review

## Description
自动化代码审查技能——检查代码质量、安全性、性能问题，生成可操作的审查报告。

## Usage
将此技能挂载到Claude Code或Codex中，在PR审查时自动执行。

## Instructions

1. 分析代码变更（diff或完整文件）
2. 检查以下维度：
   - 代码正确性：逻辑错误、边界条件
   - 安全性：注入漏洞、敏感信息泄露
   - 性能：不必要的循环、内存泄漏、N+1查询
   - 可维护性：命名规范、函数长度、注释质量
   - 测试覆盖：关键路径是否缺少测试
3. 生成分级报告：
   - 🔴 Critical: 必须修复
   - 🟡 Warning: 建议修复
   - 🔵 Info: 优化建议
4. 为每个问题提供具体的修复建议和代码示例

## Compatible Agents
- claude-code
- codex
- gemini
