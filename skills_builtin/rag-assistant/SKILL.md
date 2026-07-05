# rag-assistant

## Description
RAG知识库助手——为自定义知识库提供检索增强生成能力。

## Instructions

1. 初始化知识库（从文档/数据库/API加载）
2. 对输入查询进行向量化检索
3. 检索Top-K最相关文档片段
4. 基于检索结果生成准确回答
5. 标注引用来源
6. 对不确定性高的回答标注置信度
7. 支持增量更新知识库

## Configuration
- embedding_model: 默认使用text-embedding-3-small
- chunk_size: 512
- chunk_overlap: 50
- top_k: 5
- similarity_threshold: 0.7

## Compatible Agents
- claude-code
- gemini
