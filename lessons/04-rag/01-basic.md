# RAG 基础

## RAG 是什么

RAG 是 Retrieval-Augmented Generation，中文常叫检索增强生成。

它的核心思想是：

```text
先从知识库检索相关资料，再让模型基于资料回答。
```

这和直接把问题丢给模型不同。模型不一定知道你的私有文档，但 RAG 可以先把相关内容找出来，再交给模型使用。

## 为什么需要 RAG

LLM 有几个问题：

- 不知道你的私有知识
- 训练数据可能过时
- 容易编造看似合理的答案
- 长文档不能无限塞进上下文

RAG 可以缓解这些问题。

## 基本流程

```text
文档加载
  ↓
文档切分
  ↓
生成 embedding
  ↓
存入向量数据库
  ↓
用户提问
  ↓
检索相关 chunk
  ↓
拼接上下文
  ↓
模型生成回答
  ↓
返回答案和来源
```

## Document Loader

Document Loader 负责读取原始资料。

常见来源：

- Markdown
- PDF
- Word
- HTML
- Notion
- 数据库
- 代码文件

## Chunking

Chunking 是把长文档切成小块。

切太大：检索不精准，浪费 token。

切太小：上下文不完整，回答容易缺信息。

常见策略：

- 按标题切
- 按段落切
- 固定长度切
- 带 overlap 的滑动窗口

## Embedding

Embedding 是把文本转换成向量，方便计算语义相似度。

用户问题也会被转换成向量，然后和文档 chunk 向量做相似度匹配。

## Vector Database

向量数据库用于存储和检索 embedding。

常见选择：

- Chroma
- FAISS
- Milvus
- Pinecone
- Weaviate
- pgvector

## Embedding 设计

Embedding 不是“越高级越好”，而是要和 chunk、检索目标、成本一起设计。

建议记录：

- embedding 模型名和维度。
- chunk 的 `chunk_id`、`document_id`、标题、章节、行号。
- 文档版本或内容 hash，便于判断是否需要重新生成向量。
- 生成时间和失败原因，便于增量更新。

常见注意点：

- chunk 内容变化后必须重新 embedding。
- query embedding 和 document embedding 应使用兼容模型。
- 过短 chunk 可能缺上下文，过长 chunk 可能语义混杂。
- 教学或测试环境可以先用 mock embedding，但接口要保留真实替换能力。

## Vector Store 设计

Vector Store 至少要能保存向量和 metadata。metadata 决定了后续是否能解释来源、过滤范围和调试检索结果。

推荐字段：

```json
{
  "chunk_id": "rag.md#003",
  "document_id": "rag.md",
  "source": "knowledge_base/rag.md",
  "section": "检索阶段",
  "start_line": 20,
  "end_line": 36,
  "content_hash": "...",
  "embedding_model": "embedding-model-name"
}
```

选型建议：

- 小型教学项目：JSON + 本地向量文件，便于理解。
- 单机进阶项目：SQLite / FAISS / Chroma。
- 多用户或生产项目：pgvector、Milvus、Pinecone、Weaviate 等。

无论选择哪种，都要支持删除索引后完整重建，避免旧向量污染结果。

## Rerank

初次检索结果不一定最准确，Rerank 会对候选结果重新排序。

适合对准确率要求更高的场景。

典型做法：

```text
query → 初检 Top 20 → rerank → 取 Top 3-5 → 组装上下文
```

Rerank 可以使用规则、交叉编码器、专用 rerank 模型或 LLM 判断。教学阶段可以先用规则：标题命中、关键词命中、chunk 长度、来源可信度等。

不要把 rerank 当成万能修复。如果初检召回不到正确 chunk，rerank 无法凭空找回。

## Citation

Citation 是来源引用。

好的 RAG 回答应该告诉用户：答案来自哪个文档、哪个章节或哪个 chunk。

## Query Rewrite

用户问题可能很口语化，Query Rewrite 会先把问题改写成更适合检索的形式。

## Retrieval Eval

RAG 需要单独评测检索，而不是只看最终回答。建议维护一组问题：

```json
{
  "question": "RAG 为什么需要引用？",
  "expected_sources": ["knowledge_base/rag.md"],
  "expected_sections": ["Citation"],
  "should_answer": true
}
```

关键指标：

- Top K 命中率：正确来源是否出现在前 K 个结果中。
- MRR：正确结果越靠前越好。
- 无答案拒答率：知识库外问题是否拒绝编造。
- 引用准确率：答案引用是否真的支持结论。
- 检索调试可见性：能否看到 query、候选 chunk、分数、rerank 原因。

## 一句话总结

RAG 的重点不是让模型记住全部知识，而是让模型在回答前先查到正确资料。
