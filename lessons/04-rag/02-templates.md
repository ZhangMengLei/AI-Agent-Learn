# RAG 常用模板

## 文档 chunk 记录模板

```json
{
  "chunk_id": "doc1-0001",
  "document_id": "doc1",
  "title": "Agent 入门",
  "section": "什么是 Agent",
  "content": "Agent 是能够围绕目标自主调用工具并推进任务的系统。",
  "metadata": {
    "source": "agent-intro.md",
    "page": null,
    "created_at": "2026-06-30"
  }
}
```

## RAG 检索流程模板

```text
1. 接收用户问题
2. 对问题做必要改写
3. 生成问题 embedding
4. 从向量库检索 top_k 个 chunk
5. 可选：对结果 rerank
6. 过滤低相关结果
7. 组装上下文
8. 调用 LLM 生成回答
9. 返回回答和引用来源
```

## 检索结果模板

```json
[
  {
    "chunk_id": "doc1-0001",
    "score": 0.86,
    "source": "agent-intro.md",
    "content": "Agent 是能够围绕目标自主调用工具并推进任务的系统。"
  }
]
```

## 回答 Prompt 模板

```text
你是一个知识库问答助手。

请只基于下面提供的资料回答用户问题。

要求：
1. 如果资料不足，请回答“根据当前资料无法确定”
2. 不要编造资料中没有的信息
3. 回答后列出引用来源

用户问题：
{{question}}

资料：
{{retrieved_chunks}}
```

## 引用格式模板

```text
答案：
{{answer}}

来源：
- {{source}} / {{section}}
- {{source}} / {{section}}
```

## RAG 参数模板

```json
{
  "chunk_size": 800,
  "chunk_overlap": 100,
  "top_k": 5,
  "score_threshold": 0.7,
  "use_rerank": true
}
```

## 检查清单

- chunk 是否保留了来源？
- 检索结果是否相关？
- Prompt 是否限制模型只基于资料回答？
- 回答是否带引用？
- 资料不足时是否会承认不知道？
