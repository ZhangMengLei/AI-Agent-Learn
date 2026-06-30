# 05 Agent 架构

## 学习目标

理解 Agent 和普通 Chatbot 的区别，掌握 Agent 的任务循环和架构模式。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习工程](04-exercises-lab/README.md)
- [实战项目](05-project.md)
- [项目工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)

## 核心概念

- Chatbot vs Agent
- Goal / Plan / Act / Observe / Reflect / Finish
- ReAct Agent
- Planner-Executor
- Memory
- Tools
- Evaluator
- Permission System
- 最大迭代限制
- State Persistence
- Checkpoint / Resume
- Failure Recovery
- Trace / Observation Log

## 学习任务

1. 理解 Agent 的基本循环。
2. 实现一个最小 ReAct Agent。
3. 为 Agent 添加工具调用记录。
4. 为 Agent 添加终止条件。
5. 设计一个自动研究助手。
6. 将 Agent state 持久化，支持从 checkpoint 恢复。
7. 为工具失败、模型失败和达到迭代上限设计恢复策略。
8. 输出可观测日志，能追踪每一步 plan、action、observation 和 decision。

## 进阶路线

Agent 从 demo 走向可靠系统，关键是可恢复和可观测：

1. State：用结构化对象保存 goal、plan、current_step、observations、tool_logs、decisions、finished。
2. Persistence：每轮迭代后写 checkpoint，避免中途失败后从头开始。
3. Recovery：区分可重试失败、不可重试失败、需要人工确认的失败。
4. Observability：为每一步生成 trace id，记录输入、工具、耗时、结果摘要和下一步决策。
5. Safety：高风险工具调用前必须确认，日志脱敏，不把密钥交给模型。
6. Evaluation：用 rubric 评估计划质量、工具选择、引用质量、最终报告质量。

## 实战项目

做一个自动研究助手。
