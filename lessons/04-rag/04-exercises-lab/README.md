# RAG 练习工程说明

本练习工程用于把 RAG 的核心流程拆成几个可运行的小实验：读取本地 Markdown、切分 chunk、建立检索索引、根据问题找回相关片段，并在回答中给出引用。

本阶段不追求复杂框架，建议先用本地文件和简单相似度算法跑通流程，再替换为真实 embedding 模型或向量数据库。

## 练习目标

完成后你应该能够：

1. 从本地 Markdown 知识库读取文档。
2. 按标题和长度切分文档 chunk。
3. 为每个 chunk 保存来源、标题、章节等 metadata。
4. 根据用户问题检索 Top K 相关片段。
5. 组装包含引用的回答 Prompt。
6. 在资料不足时明确回答“不知道”。

## 推荐目录

建议在本目录下创建自己的实验代码，例如：

```text
04-exercises-lab/
  README.md
  src/
    ingest.py              # 读取 Markdown 并生成 chunk
    chunker.py             # chunk 切分逻辑
    retriever.py           # 简单检索逻辑
    ask.py                 # 问答入口
    citations.py           # 引用格式化
    prompts/
      answer_prompt.txt
  knowledge_base/
    ai-agent.md
    tool-use.md
    rag.md
  index/
    chunks.json            # ingest 后生成的 chunk 数据
  tests/
    test_chunker.py
    test_retriever.py
```

不要把 API Key 写进项目文件。如果接入真实模型，请使用环境变量读取。

## 实验 1：准备本地 Markdown 知识库

在 `knowledge_base/` 中准备 3 篇左右 Markdown 文档，例如：

```text
ai-agent.md      Agent 基础概念
tool-use.md      工具调用说明
rag.md           RAG 流程说明
```

每篇文档建议包含：

- 一级标题。
- 二级标题。
- 2 到 5 个短段落。
- 明确可被提问的事实。

示例问题：

```text
RAG 为什么需要 chunk？
工具调用和 RAG 有什么区别？
Agent 为什么需要规划？
```

## 实验 2：实现 ingest

`ingest.py` 负责读取 Markdown 并输出统一 chunk 数据。

建议输出结构：

```json
{
  "chunk_id": "rag.md#chunk-001",
  "document_id": "rag.md",
  "title": "RAG 流程说明",
  "section": "检索阶段",
  "content": "检索阶段会根据用户问题找到相关文档片段。",
  "source": "knowledge_base/rag.md",
  "start_line": 12,
  "end_line": 18
}
```

练习阶段可以先不做 embedding，直接把所有 chunk 写入 `index/chunks.json`。

## 实验 3：实现 chunk

建议先使用混合策略：

1. 优先按 Markdown 标题分段。
2. 如果某段太长，再按字符长度切分。
3. 相邻 chunk 保留少量 overlap，避免上下文断裂。

推荐初始参数：

```text
chunk_size: 500 到 800 个中文字符
overlap: 50 到 100 个中文字符
```

每个 chunk 必须带 metadata，至少包括：

- 文档名。
- 标题。
- 章节。
- 来源路径。
- chunk 编号。

## 实验 4：实现检索

初学阶段可以用关键词重叠实现简单检索：

```text
score = 问题词与 chunk 内容词的重合数量
```

也可以使用本地 embedding 或第三方 embedding，但不强制。

检索函数建议形式：

```text
retrieve(query, top_k=3) -> list[chunk]
```

返回结果应按相关度排序，并保留分数，方便调试：

```json
{
  "score": 0.82,
  "chunk_id": "rag.md#chunk-001",
  "content": "...",
  "source": "knowledge_base/rag.md",
  "section": "检索阶段"
}
```

## 实验 5：实现带引用问答

回答时不要只把 chunk 内容拼接给模型，而要加明确约束：

```text
你只能基于给定资料回答。
如果资料不足，请回答“根据当前资料无法确定”。
回答后必须列出引用来源。
```

引用格式建议：

```text
答案正文……

引用：
[1] knowledge_base/rag.md - 检索阶段
[2] knowledge_base/tool-use.md - 工具调用链路
```

如果暂时不接入模型，可以先做模板化回答：输出 Top 1 chunk 摘要和引用，验证检索链路是否正确。

## 运行方式

推荐命令如下，可按你的实现调整：

```bash
cd lessons/04-rag/04-exercises-lab
python src/ingest.py --input knowledge_base --output index/chunks.json
python src/ask.py "RAG 为什么要切分 chunk？"
```

建议每次修改 chunk 参数后重新运行 ingest，并观察检索结果是否变化。

## 参考答案说明

本练习没有唯一答案。一个合格实现应满足：

- 能从本地 Markdown 生成 chunk。
- chunk 内容不会过长或过短。
- 每个 chunk 都能追溯到原始文档和章节。
- 检索结果和问题有明显相关性。
- 回答中包含引用。
- 资料不足时不会编造答案。

## 验收标准

- 至少导入 3 篇 Markdown 文档。
- ingest 后能生成 `chunks.json` 或等价索引文件。
- 任意输入一个问题，能返回 Top K 检索片段。
- 最终回答包含来源引用。
- 对知识库外的问题能回答“无法确定”或“不知道”。
- 能打印检索调试信息：chunk_id、score、source。
