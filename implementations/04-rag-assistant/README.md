# 本地 Markdown RAG 教学 Demo

这个目录演示一个完全本地、可运行、无外部依赖的 RAG（Retrieval-Augmented Generation，检索增强生成）最小系统。

它只使用 Python 标准库：不调用 embedding API，不调用真实 LLM，也不需要向量数据库。目标是帮助理解 RAG 的核心流程，而不是追求生产级效果。

## RAG 流程

本 Demo 的流程如下：

```text
data/docs/*.md
  ↓
加载 Markdown 文档
  ↓
按标题和段落切分 chunk
  ↓
为每个 chunk 记录 metadata
  ↓
对用户问题做关键词抽取
  ↓
用关键词重叠和简单打分检索 chunk
  ↓
把命中的片段拼接成 mock 回答
  ↓
输出答案和引用来源
```

对应到代码：

- `load_documents()`：读取 `data/docs/*.md`。
- `chunk_documents()`：按 Markdown 标题和段落切分文本。
- `metadata`：记录来源文件、文档标题、章节、段落序号、字符位置。
- `search()`：用关键词命中、覆盖率、频次、标题命中奖励进行排序。
- `generate_mock_answer()`：把检索片段拼接成回答，并输出引用。

## 运行方式

在仓库根目录运行：

```bash
python implementations/04-rag-assistant/main.py "Agent 和 Chatbot 区别是什么"
```

也可以指定文档目录和返回片段数量：

```bash
python implementations/04-rag-assistant/main.py "RAG 为什么需要引用" --docs-dir data/docs --top-k 2
```

## 文档目录

默认读取：

```text
data/docs/*.md
```

如果你的仓库原本没有 `data/docs`，本 Demo 提供了最小样例文档：

- `data/docs/agent-vs-chatbot.md`
- `data/docs/rag-basics.md`

你可以继续添加自己的 Markdown 文件。程序会自动读取该目录下所有 `.md` 文件。

## 引用格式

回答中的引用格式类似：

```text
[C3] agent-vs-chatbot.md > 核心区别
```

含义是：

- `C3`：chunk ID。
- `agent-vs-chatbot.md`：来源文件。
- `核心区别`：来源章节。

在引用列表中还会输出 `score` 和 `matched`，用于教学时观察检索为什么命中。

## 局限

这个 Demo 故意保持简单，因此有明显局限：

1. 关键词检索只能匹配字面词，不能理解复杂语义。
2. 中文分词使用简化的 bigram/trigram 方式，不如专业分词器准确。
3. mock 回答只是拼接摘要，不具备真实 LLM 的归纳、推理和改写能力。
4. 没有向量索引，文档很多时检索效率会下降。
5. 没有 rerank、权限过滤、增量索引、缓存和评测体系。

## 如何替换为真实 embedding / LLM

可以按下面顺序逐步升级：

1. 替换 `tokenize()` 和 `search()`：
   - 对每个 chunk 调用 embedding 模型生成向量。
   - 对用户 query 生成 query 向量。
   - 用余弦相似度或向量数据库检索 top-k。

2. 增加向量存储：
   - 小规模可用本地 JSON / SQLite 保存向量。
   - 中大型项目可接入 FAISS、Chroma、Milvus、pgvector 等。

3. 替换 `generate_mock_answer()`：
   - 把 top-k chunk 拼成上下文。
   - 设计提示词，要求模型只基于上下文回答。
   - 要求模型保留引用 ID，例如 `[C3]`。

4. 增加质量控制：
   - 检索命中不足时拒答或要求补充信息。
   - 对答案做引用一致性检查。
   - 建立离线测试集，评估召回率、准确率和幻觉率。

## 运行测试

在仓库根目录运行：

```bash
python -m unittest tests/test_rag_assistant.py
```
