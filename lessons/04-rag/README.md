# 04 RAG 知识库问答

## 学习目标

让模型基于私有文档回答问题，减少幻觉，并给出来源引用。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习工程](03-exercises-lab/README.md)
- [实战项目](04-project.md)
- [项目工程](04-project-lab/README.md)
- [阶段复盘](05-review.md)

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

## 学习任务

1. 加载 Markdown 或 PDF 文档。
2. 将文档切分成 chunk。
3. 生成 embedding 并存入向量库。
4. 根据问题检索相关片段。
5. 将检索结果交给模型回答。
6. 在回答中附带来源。

## 实战项目

做一个文档知识库问答助手。
