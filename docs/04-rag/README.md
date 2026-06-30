# 04 RAG 知识库问答

## 学习目标

让模型基于私有文档回答问题，减少幻觉，并给出来源引用。

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

## 常见组件

- Chroma
- FAISS
- Milvus
- Pinecone
- Weaviate
- pgvector
- LangChain
- LlamaIndex

## 学习任务

1. 加载一个 PDF 或 Markdown 文档。
2. 把文档切分成 chunk。
3. 生成 embedding 并存入向量库。
4. 根据问题检索相关片段。
5. 把检索结果交给模型回答。
6. 在回答中附带来源。

## 实战项目

做一个 `文档知识库问答助手`：

- 支持导入文档
- 支持自然语言提问
- 支持来源引用
- 支持多文档检索

## 检查标准

- 检索结果是否真的相关？
- 回答是否只基于文档？
- 是否能指出不知道？
- 是否能追溯来源？
