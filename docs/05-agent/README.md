# 05 Agent 架构

## 学习目标

理解 Agent 和普通 Chatbot 的区别，掌握 Agent 的任务循环和架构模式。

## Chatbot 与 Agent

普通 Chatbot：用户问，模型答。

Agent：用户给目标，模型拆解任务、调用工具、观察结果，并持续推进直到完成。

## 核心循环

```text
Goal → Plan → Act → Observe → Reflect → Finish
```

## 常见架构

- ReAct Agent
- Planner-Executor
- Reflection Agent
- Multi-Agent
- Code Agent
- Browser Agent
- Workflow Agent

## 核心组件

- LLM
- Tools
- Memory
- Planner
- Executor
- Evaluator
- Permission System

## 学习任务

1. 实现一个 ReAct 风格的最小 Agent。
2. 让 Agent 能调用 2 个以上工具。
3. 给 Agent 增加任务步骤记录。
4. 给 Agent 增加最大迭代次数，避免无限循环。
5. 增加任务完成判断。

## 实战项目

做一个 `自动研究助手`：

- 接收一个主题
- 拆成多个子问题
- 调用搜索或文档工具
- 汇总结果
- 生成报告

## 常见问题

- Agent 容易跑偏。
- 成本和耗时不可控。
- 工具调用可能失败。
- 任务是否完成很难判断。
- 权限设计非常重要。
