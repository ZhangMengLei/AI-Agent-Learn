# AI 基础练习实验工程

这个 lab 不要求写复杂代码，目标是把 AI 相关概念整理成你自己的学习地图。

## 目标

完成一个 `ai-learning-map.md`，说明：

- AI / ML / DL / LLM 的关系。
- Chatbot / RAG / Agent / MCP 的区别。
- Prompt、token、上下文、幻觉的含义。
- 开发中使用 AI 的安全边界。
- 你后续最想完成的 AI 项目。

## 建议目录

```text
my-ai-foundation-lab/
  ai-learning-map.md
  glossary.md
  use-case-decisions.md
```

## 步骤

### 1. 写概念地图

在 `ai-learning-map.md` 中画出：

```text
用户问题
  -> Prompt
  -> LLM
  -> 可选：RAG / Tool / Agent / MCP
  -> 输出
  -> Eval / Security 检查
```

### 2. 写术语表

在 `glossary.md` 中至少解释 12 个术语：

- AI
- ML
- DL
- LLM
- Prompt
- Token
- Context Window
- Hallucination
- Embedding
- RAG
- Tool Use
- Agent
- MCP
- Eval

### 3. 做方案判断

在 `use-case-decisions.md` 中选择 5 个真实开发需求，判断该用：

- Prompt
- LLM API
- RAG
- Tool Use
- Agent
- MCP
- Claude Code

每个需求写明为什么。

## 验收标准

- 能用自己的话解释核心术语。
- 能判断常见需求适合哪种 AI 方案。
- 能说出至少 5 条安全边界。
- 不包含真实 API Key、token、cookie 或生产数据。
