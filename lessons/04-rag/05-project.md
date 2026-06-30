# RAG 实战项目：文档知识库问答助手

## 项目目标

做一个可以导入本地文档并基于文档回答问题的知识库助手。

## 功能要求

### 基础功能

- 支持导入 Markdown 文档
- 自动切分文档
- 生成 embedding
- 存入向量库
- 根据问题检索相关内容
- 调用 LLM 生成回答
- 回答附带来源引用

### 进阶功能

- 支持 PDF
- 支持多文档检索
- 支持 embedding 相似度检索
- 支持可重建的 vector store
- 支持 hybrid search：关键词 + 向量
- 支持 rerank
- 支持检索结果调试
- 支持回答质量评分
- 支持 retrieval eval：期望引用、Top K 命中率和无答案拒答率

## 推荐目录

```text
rag-assistant/
  README.md
  ingest.py
  ask.py
  documents/
  vector_store/
  prompts/
  logs/
```

## 核心流程

### 导入阶段

```text
读取文档
  ↓
清洗文本
  ↓
切分 chunk
  ↓
生成 embedding
  ↓
保存到向量库
```

### 问答阶段

```text
用户提问
  ↓
问题向量化
  ↓
检索相关 chunk
  ↓
组装 Prompt
  ↓
调用模型
  ↓
返回答案和来源
```

## Index 与检索设计

### Chunk metadata

每个 chunk 必须带 metadata，避免最后只能回答却无法解释来源：

```json
{
  "chunk_id": "doc-001#005",
  "document_id": "doc-001",
  "source": "documents/rag.md",
  "section": "Rerank",
  "start_line": 42,
  "end_line": 58,
  "content_hash": "..."
}
```

### Embedding 与 vector store

建议把 embedding 逻辑封装为 `Embedder`，把存储封装为 `VectorStore`：

```text
Embedder.embed_documents(chunks) -> vectors
Embedder.embed_query(question) -> query_vector
VectorStore.upsert(chunks, vectors)
VectorStore.search(query_vector, top_k, filters)
```

教学阶段可以使用 mock embedding 或简单向量；进阶阶段再替换为真实 embedding API。本地索引目录应支持删除后重建，避免旧文档残留。

### Rerank 流程

推荐检索策略：

```text
关键词召回 Top 20
  + 向量召回 Top 20
  ↓
合并去重
  ↓
rerank
  ↓
取 Top 3-5 进入 Prompt
```

`inspect` 命令应打印初检分数、rerank 分数、来源和片段预览，帮助判断问题出在召回还是排序。

## 验收标准

- 至少导入 3 篇文档。
- 能对文档内容进行问答。
- 回答中包含引用来源。
- 资料不足时能回答不知道。
- 能打印检索到的 chunk，方便调试。
- 能重建索引并确认旧 chunk 不污染新结果。
- 至少准备 5 条 retrieval eval case，记录期望来源和 Top K 是否命中。

## 扩展方向

- 增加 Web UI。
- 增加文档增量更新。
- 增加混合检索：关键词 + 向量。
- 增加用户反馈：有用 / 无用。
- 增加评测集，持续评估回答质量。
