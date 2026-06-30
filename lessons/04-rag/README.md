# 04 RAG 知识库问答

## 学习目标

让模型基于私有文档回答问题，减少幻觉，并给出来源引用。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习工程](04-exercises-lab/README.md)
- [实战项目](05-project.md)
- [项目工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)

## 核心概念

- RAG：Retrieval-Augmented Generation
- Document Loader
- Chunking
- Embedding
- Vector Database
- Similarity Search
- Rerank
- Citation
- Query Rewrite
- Hybrid Search：关键词 + 向量
- Metadata Filter
- Index Refresh
- Retrieval Eval

## 学习任务

1. 加载 Markdown 或 PDF 文档。
2. 将文档切分成 chunk。
3. 生成 embedding 并存入向量库。
4. 根据问题检索相关片段。
5. 将检索结果交给模型回答。
6. 在回答中附带来源。

## 进阶路线

RAG 的进阶重点不是“把文档塞给模型”，而是把检索链路做成可调试、可评测、可替换的系统。

```text
Loader → Cleaner → Chunker → Embedder → Vector Store → Retriever → Reranker → Prompt Builder → Answerer → Citation → Eval
```

建议逐步升级：

1. 先用关键词或本地 JSON 索引跑通知识库问答。
2. 加入 embedding，把 query 和 chunk 转成向量。
3. 选择本地向量库或轻量 vector store，保存向量和 metadata。
4. 支持 hybrid search：关键词召回 + 向量召回。
5. 对候选 Top 20 做 rerank，再取 Top 3-5 进入 Prompt。
6. 为每个答案记录命中的 chunk、引用和资料不足判断。
7. 建立 retrieval eval：问题、期望引用、命中率、无答案拒答率。

## 实战项目

做一个文档知识库问答助手。
