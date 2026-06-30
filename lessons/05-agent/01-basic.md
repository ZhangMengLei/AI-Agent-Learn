# Agent 架构基础

## Chatbot 和 Agent 的区别

普通 Chatbot 的工作方式是：

```text
用户提问 → 模型回答
```

Agent 的工作方式更接近：

```text
用户给目标 → Agent 拆解任务 → 调用工具 → 观察结果 → 继续行动 → 完成目标
```

Chatbot 更像问答助手，Agent 更像能执行任务的工作流系统。

## Agent 的核心循环

```text
Goal → Plan → Act → Observe → Reflect → Finish
```

### Goal

用户给出的最终目标。

例如：

```text
帮我研究 MCP 是什么，并写一份入门总结。
```

### Plan

Agent 将目标拆成步骤。

例如：

1. 查询 MCP 基础定义
2. 整理核心概念
3. 总结使用场景
4. 写成学习笔记

### Act

执行某一步动作，可能是调用工具、读取文件、搜索资料或生成内容。

### Observe

观察动作结果。

工具返回的数据、命令输出、文件内容都属于观察结果。

### Reflect

判断当前结果是否足够，是否需要调整计划。

### Finish

输出最终结果并停止。

## ReAct Agent

ReAct 是 Reason + Act。

它让模型交替进行：

```text
思考 → 行动 → 观察 → 再思考
```

适合需要多步推理和工具调用的任务。

## Planner-Executor

Planner-Executor 把计划和执行分开：

- Planner：负责拆解任务
- Executor：负责执行具体步骤

优点是结构清晰，适合复杂任务。

## Memory

Memory 用来保存任务过程中的信息。

常见类型：

- 短期记忆：当前任务上下文
- 长期记忆：用户偏好、历史知识
- 工作记忆：当前计划、工具结果、待办事项

## Evaluator

Evaluator 用来判断任务是否完成、结果是否合格。

它可以是规则，也可以是另一个模型。

## Permission System

Agent 能调用工具，所以必须有权限系统。

低风险动作可以自动执行，高风险动作需要人工确认。

## 最大迭代限制

Agent 可能陷入循环，所以必须设置最大迭代次数。

例如：

```text
最多执行 10 步，超过后停止并说明当前进展。
```

## State Persistence

Agent 不能只把状态放在模型上下文里。模型上下文会变长、会被裁剪，也无法在程序崩溃后恢复。建议把 Agent state 设计成结构化对象，并在每轮迭代后持久化。

最小 state 字段：

```json
{
  "run_id": "run-001",
  "goal": "研究 RAG 的核心流程",
  "plan": ["检索资料", "阅读资料", "总结结论"],
  "current_step": 1,
  "observations": [],
  "tool_logs": [],
  "decisions": [],
  "finished": false,
  "error": null
}
```

持久化建议：

- 每次 plan、act、observe、reflect 后写 checkpoint。
- checkpoint 使用 JSON 或 SQLite，教学阶段 JSON 足够。
- 写入时避免保存真实密钥、cookie、完整隐私输入。
- `run_id` 和 `trace_id` 要能把日志、报告和状态串起来。

## 失败恢复

Agent 失败不应该只有“崩溃退出”。至少区分：

| 失败类型 | 示例 | 处理方式 |
| --- | --- | --- |
| 可重试 | 临时超时、限流 | 有限重试，记录 retry_count |
| 不可重试 | 参数 schema 错、工具不存在 | 停止当前动作，要求修正计划 |
| 需要人工确认 | 写文件、发消息、执行高风险命令 | 暂停并等待确认 |
| 资料不足 | 检索无结果 | 调整 query 或明确无法完成 |
| 达到上限 | 超过 max_iterations | 输出当前进展和未完成事项 |

恢复策略示例：

```text
读取 latest checkpoint
  ↓
检查 finished / error / current_step
  ↓
如果上一步工具成功但未反映到报告，继续 reflect
  ↓
如果上一步失败可重试且 retry_count 未超限，重试
  ↓
否则安全停止并输出可恢复说明
```

## 可观测日志

每一步都应该能回答：Agent 为什么这样做？调用了什么？结果是什么？下一步是什么？

建议日志字段：

```json
{
  "run_id": "run-001",
  "trace_id": "step-003",
  "phase": "act",
  "tool_name": "search_notes",
  "input_preview": "RAG 核心流程",
  "ok": true,
  "duration_ms": 120,
  "output_preview": "找到 3 条资料",
  "decision": "继续阅读最相关资料"
}
```

日志要服务于排障和复盘，不要记录 API Key 或敏感全文。

## 一句话总结

Agent 的本质是围绕目标持续执行：计划、行动、观察、调整，直到完成或停止。
