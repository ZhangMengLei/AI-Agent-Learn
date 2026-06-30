# RAG 项目实现工程说明

本项目实验要求你实现一个本地 Markdown 知识库问答助手。它能够导入本地文档，切分并索引内容，根据用户问题检索相关 chunk，并生成带来源引用的回答。

项目重点是完整 RAG 工程链路：ingest、chunk、检索、组装上下文、回答和引用。

## 项目目标

实现一个命令行版 Local Markdown RAG Assistant，具备以下能力：

1. 扫描本地 Markdown 知识库目录。
2. 将文档切分为带 metadata 的 chunk。
3. 建立可重复生成的本地索引。
4. 根据问题检索 Top K 相关 chunk。
5. 基于检索资料生成回答。
6. 在回答中列出引用来源。
7. 当资料不足时拒绝编造。

## 推荐文件结构

可以在本目录下按下面结构实现：

```text
04-project-lab/
  README.md
  pyproject.toml 或 package.json
  src/
    cli.py                    # 命令行入口：ingest / ask / inspect
    config.py                 # chunk 参数、top_k 等配置
    loaders/
      markdown_loader.py      # Markdown 文档读取
    chunking/
      markdown_chunker.py     # 标题 + 长度切分
    indexing/
      index_store.py          # 本地索引读写
      embeddings.py           # 可选：embedding 封装
    retrieval/
      retriever.py            # 检索 Top K
      reranker.py             # 可选：重排
    generation/
      prompt_builder.py       # 组装回答 Prompt
      answerer.py             # 调用模型或 mock 回答
      citations.py            # 引用生成
    evaluation/
      eval_cases.json         # 简单评测问题
      run_eval.py             # 可选：批量验证
  knowledge_base/
    getting-started.md
    tool-use.md
    rag.md
  index/
    chunks.json
    vectors.json              # 可选
```

如果你想先做最小版本，可以只实现：

```text
src/cli.py
src/markdown_loader.py
src/chunker.py
src/retriever.py
src/prompt_builder.py
src/citations.py
knowledge_base/
index/
```

## 命令设计

建议提供三个命令：

```bash
python src/cli.py ingest --input knowledge_base --index index
python src/cli.py ask "RAG 的核心流程是什么？" --index index --top-k 3
python src/cli.py inspect --index index --query "如何给回答加引用？"
```

命令含义：

- `ingest`：重新读取文档、切分 chunk、写入索引。
- `ask`：检索并生成最终回答。
- `inspect`：只展示检索结果，不生成回答，用于调试。

## 核心模块实现步骤

### 第 1 步：Markdown Loader

读取 `knowledge_base/` 下的 `.md` 文件。

建议保留：

- 文件路径。
- 文件名。
- 原始文本。
- 标题。
- 行号信息。

注意：只读取知识库目录内文件，不要支持任意绝对路径读取。

### 第 2 步：Chunker

推荐策略：标题优先，长度兜底。

```text
按 Markdown 标题切分
  ↓
段落过长时按 chunk_size 二次切分
  ↓
为相邻片段保留 overlap
  ↓
写入 metadata
```

每个 chunk 建议包含：

```json
{
  "chunk_id": "tool-use.md#003",
  "document_id": "tool-use.md",
  "title": "工具调用说明",
  "section": "权限确认",
  "content": "...",
  "source": "knowledge_base/tool-use.md",
  "start_line": 30,
  "end_line": 45
}
```

### 第 3 步：Index Store

最小版本可以使用 JSON 文件：

```text
index/chunks.json
```

进阶版本可以加入：

- `vectors.json`：保存 embedding 向量。
- SQLite：保存 chunk 和 metadata。
- 向量数据库：保存向量并支持相似度搜索。

无论哪种方式，都要保证索引可以删除后重新生成。

### 第 4 步：Retriever

最小版本：关键词重叠、BM25 或简单打分。

进阶版本：embedding 相似度。

检索结果必须包含：

- `chunk_id`
- `score`
- `content`
- `source`
- `section`

建议在 `inspect` 命令中打印这些字段，便于判断检索是否正确。

### 第 5 步：Prompt Builder

Prompt 中应明确：

- 只能使用检索资料回答。
- 不确定时说明资料不足。
- 不要使用资料外知识补全。
- 回答后给出引用。

推荐结构：

```text
系统要求：只基于资料回答。
用户问题：...
检索资料：
[1] source=... section=...
内容：...
[2] source=... section=...
内容：...
输出格式：答案 + 引用
```

### 第 6 步：Answerer 与 Citations

如果接入真实大模型：

- 不要写真实 API Key。
- 从环境变量读取配置。
- 对空检索结果直接返回“根据当前资料无法确定”。

如果暂时不用模型：

- 可以将 Top K chunk 摘要拼接为回答。
- 仍然必须生成引用列表。

引用格式示例：

```text
引用：
[1] knowledge_base/rag.md - 检索阶段
[2] knowledge_base/tool-use.md - 工具调用链路
```

## 验收方式

准备至少 5 个测试问题：

1. 3 个知识库内问题，例如“RAG 包含哪些步骤？”
2. 1 个跨文档问题，例如“Tool Use 和 RAG 有什么区别？”
3. 1 个知识库外问题，例如“今天上海天气怎么样？”

逐项检查：

- `ingest` 能稳定生成索引。
- `inspect` 能显示相关 chunk、分数和来源。
- `ask` 的答案主要来自检索资料。
- 每个答案都有引用。
- 知识库外问题不会被编造回答。
- 修改文档后重新 ingest，答案能反映最新内容。

## 常见扩展

- 增加增量索引：只处理发生变化的 Markdown。
- 增加混合检索：关键词 + embedding。
- 增加 rerank：对 Top 20 结果重排后取 Top 5。
- 增加引用行号：让来源更可验证。
- 增加评测集：记录问题、期望引用和是否命中。
- 把 RAG 封装成工具，接入上一阶段的 Tool Use Assistant。
