# AI 学习导航卡片项目实验

本 lab 帮你把 `05-project.md` 的项目真正落地。你可以只写 Markdown，也可以做成简单 HTML 页面。

## 推荐产物

```text
ai-learning-navigator/
  README.md
  glossary.md
  decision-table.md
  safety-checklist.md
  roadmap.md
```

## 实现步骤

### 1. 写 README

说明这个导航卡片适合谁、解决什么问题、如何阅读。

### 2. 写 glossary

每个术语用下面格式：

```markdown
## Prompt

一句话：Prompt 是给模型的任务说明书。

解决什么：让模型知道要做什么、怎么输出。

例子：让模型按 JSON 输出需求字段。

容易误解：Prompt 不能保证事实正确，还需要验证。
```

### 3. 写 decision-table

至少列出 10 个开发或学习需求，并判断适合的 AI 技术：

- Prompt
- LLM API
- Tool Use
- RAG
- Agent
- MCP
- Claude Code
- Eval / Security

### 4. 写 safety-checklist

分成三类：

- 输入给 AI 前检查。
- AI 输出后检查。
- 提交或上线前检查。

### 5. 写 roadmap

把后续课程链接进去：

1. [Prompt](../../01-prompt/README.md)
2. [LLM API](../../02-llm-api/README.md)
3. [Tool Use](../../03-tool-use/README.md)
4. [RAG](../../04-rag/README.md)
5. [Agent](../../05-agent/README.md)
6. [MCP](../../06-mcp/README.md)
7. [Claude Code](../../07-claude-code/README.md)
8. [Eval / Security](../../08-eval-security/README.md)

## 自测问题

- 另一个小白能不能只看你的导航就知道下一步学什么？
- 每个术语是否都有例子？
- 方案选择是否说明了风险？
- 是否没有真实 API Key、token、cookie、生产数据？

## 可选扩展

- 做一个单页 HTML。
- 给每个术语配一个图。
- 把 decision table 做成问答流程。
- 增加“开发中如何使用 AI”的入口：[developer-ai-workflows](../../../labs/developer-ai-workflows.md)。
