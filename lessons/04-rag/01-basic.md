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

## Rerank

初次检索结果不一定最准确，Rerank 会对候选结果重新排序。

适合对准确率要求更高的场景。

## Citation

Citation 是来源引用。

好的 RAG 回答应该告诉用户：答案来自哪个文档、哪个章节或哪个 chunk。

## Query Rewrite

用户问题可能很口语化，Query Rewrite 会先把问题改写成更适合检索的形式。

## 一句话总结

RAG 的重点不是让模型记住全部知识，而是让模型在回答前先查到正确资料。
