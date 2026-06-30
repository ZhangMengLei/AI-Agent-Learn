# 00 AI 基础练习 Lab 参考讲解

## 参考产物结构

```text
my-ai-foundation-lab/
  ai-learning-map.md
  glossary.md
  use-case-decisions.md
```

## ai-learning-map.md 示例

```text
用户提出问题
  -> Prompt 描述任务、背景、约束、输出格式
  -> LLM 生成候选回答
  -> 如果需要资料：RAG 检索文档并提供引用
  -> 如果需要行动：Tool Use 调用函数或外部系统
  -> 如果需要多步推进：Agent 规划、行动、观察、调整
  -> 如果需要标准化工具接入：MCP 暴露 tools/resources/prompts
  -> Eval / Security 检查质量、事实、安全和权限
```

## glossary.md 要点

每个术语至少要包含：

- 一句话解释。
- 它解决什么问题。
- 一个例子。
- 一个容易误解的点。

## use-case-decisions.md 示例

| 需求 | 推荐能力 | 原因 | 风险 |
| --- | --- | --- | --- |
| 总结会议纪要 | Prompt | 输入材料已给出 | 可能漏掉决定项 |
| 公司制度问答 | RAG | 需要引用制度原文 | 文档权限和更新 |
| 自动创建日报 | Tool Use / Agent | 需要读取任务和生成内容 | 越权读取数据 |
| 修复测试失败 | Claude Code / Agent | 需要读代码、改代码、跑测试 | 误改无关文件 |
| 设计 MCP 工具 | MCP | 需要标准化暴露能力 | schema 不稳定 |

## 验收说明

合格产物应该让另一个初学者能回答：

1. 我现在面对的需求适合哪种 AI 能力？
2. 为什么不直接让 Chatbot 解决全部问题？
3. 哪些地方必须人工验证？
4. 哪些信息不能发给 AI？
