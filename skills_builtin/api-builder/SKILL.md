# api-builder

## Description
API自动构建——从OpenAPI/YAML描述生成完整的REST API服务，包括路由、验证、错误处理、Swagger文档。

## Instructions

1. 解析OpenAPI 3.x规范或简要API描述
2. 生成FastAPI/Express代码骨架：
   - 路由定义
   - 请求/响应模型（Pydantic/TypeScript）
   - 输入验证
   - 错误处理中间件
   - Swagger/OpenAPI自动文档
3. 生成对应的测试用例（pytest/jest）
4. 如果指定数据库，自动生成CRUD操作

## Compatible Agents
- claude-code
- codex
- gemini
