# 05 研究助手 Agent

这是一个面向初学者的最小 Agent 教学工程，只使用 Python 标准库，不依赖真实 LLM，也不需要 API Key。

## 你会看到什么

- 本地 notes 数据：用字典模拟知识库。
- Planner：把研究主题拆成多个步骤。
- Tool Registry：统一登记和调用工具。
- max_iterations：限制最多执行多少步，避免无限循环。
- tool log：记录每一次工具调用，方便复盘。
- report 输出：生成结构化 Markdown 研究报告。

## 运行方式

在仓库根目录执行：

```bash
python implementations/05-research-agent/research_agent.py
```

默认会研究“Agent 如何完成研究任务”，并把报告保存到：

```text
implementations/05-research-agent/runs/latest-report.md
```

## 学习建议

1. 先看 `NOTE_DATABASE`，理解本地资料从哪里来。
2. 再看 `Planner.make_plan()`，理解任务如何被拆解。
3. 再看 `ResearchAgent.run()`，理解 Agent 如何循环执行。
4. 最后修改 `max_iterations`，观察报告里的停止状态变化。
