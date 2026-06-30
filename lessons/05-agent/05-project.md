# Agent 实战项目：自动研究助手

## 项目目标

做一个可以围绕主题自动拆解问题、查找资料、整理结论并生成报告的 Agent。

## 功能要求

### 基础功能

- 接收一个研究主题
- 自动拆成多个子问题
- 调用搜索或文档工具获取资料
- 汇总资料
- 生成结构化报告

### 进阶功能

- 保存每一步思考和工具结果
- 支持最大迭代次数
- 支持资料来源引用
- 支持用户中途确认计划
- 支持结果质量评估
- 支持 state checkpoint，程序中断后可恢复
- 支持工具失败重试、跳过或安全停止
- 支持可观测日志，串联 plan、action、observation、reflection

## 推荐目录

```text
research-agent/
  README.md
  main.py 或 main.js
  prompts/
    planner.md
    executor.md
    evaluator.md
  tools/
    search.py
    reader.py
    writer.py
  runs/
```

## 核心流程

```text
用户输入研究主题
  ↓
Planner 拆解任务
  ↓
用户确认计划
  ↓
Executor 执行每一步
  ↓
工具返回观察结果
  ↓
Evaluator 判断是否足够
  ↓
生成最终报告
```

## 状态、恢复与观测

### State schema

建议每次运行保存一个 `runs/<run_id>/state.json`：

```json
{
  "run_id": "research-001",
  "goal": "研究 MCP 是什么",
  "plan": [],
  "current_step": 0,
  "observations": [],
  "tool_logs": [],
  "decisions": [],
  "retry_count": {},
  "finished": false,
  "stop_reason": null
}
```

每轮迭代结束后写 checkpoint，确保程序中断后可以 resume。

### 失败恢复

必须定义每类失败怎么处理：

- 工具超时：有限重试，超过后记录失败并进入 reflection。
- 工具参数错误：不重试，要求 planner 修正下一步。
- 检索无结果：改写 query 或标记资料不足。
- 模型输出格式错误：要求重新生成结构化输出，超过次数后安全停止。
- 达到最大迭代次数：输出当前进展、已完成步骤和未完成事项。

### 观测日志

每一步写一条 JSONL 日志，字段建议包含：

```json
{
  "run_id": "research-001",
  "trace_id": "iter-003",
  "phase": "observe",
  "tool_name": "reader",
  "ok": true,
  "duration_ms": 240,
  "input_preview": "source=doc-001",
  "output_preview": "读取到 MCP 定义与使用场景",
  "next_decision": "继续汇总核心概念"
}
```

最终报告应能回溯每个关键结论来自哪些观察结果。

## 报告格式

```text
# 研究报告标题

## 一句话总结

## 核心概念

## 关键发现

## 适合初学者的理解方式

## 资料来源

## 后续学习建议
```

## 验收标准

- 能把一个主题拆成子问题。
- 能调用至少 2 个工具。
- 能记录每一步执行过程。
- 能在达到最大迭代次数后停止。
- 最终报告结构清晰，并带来源。
- 每轮迭代后能保存 state checkpoint。
- 从中断状态恢复时不会重复执行已成功的高风险动作。
- 工具失败有明确 retry / skip / stop 策略。
- 日志能按 run_id 和 trace_id 追踪完整执行链路。

## 扩展方向

- 加入 RAG 私有知识库。
- 加入网页浏览工具。
- 加入多 Agent 协作：研究员、编辑、评审。
- 为报告质量建立评分标准。
