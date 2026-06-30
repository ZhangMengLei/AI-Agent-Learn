# Agent 项目实现工程说明：最小研究助手

本项目实验用于把 05-agent 阶段的知识组合成一个可运行的小工程：最小研究助手。它不追求全自动、全联网或复杂框架，而是聚焦 Agent 工程最重要的骨架：目标输入、计划生成、行动执行、观察记录、迭代停止和结果汇总。

## 项目目标

实现一个命令行研究助手，用户输入一个主题后，系统能够：

1. 生成研究计划。
2. 按计划调用工具收集资料。
3. 记录每一步工具调用日志。
4. 根据观察结果更新任务状态。
5. 在完成任务或达到 `max_iterations` 后停止。
6. 输出一份结构化研究摘要。

推荐先使用本地模拟资料，不依赖真实搜索 API。这样更适合初学者理解 Agent 控制流。

## 推荐文件结构

```text
06-project-lab/
  README.md
  research_agent/
    main.py
    config.py
    agent.py
    state.py
    planner.py
    executor.py
    observer.py
    reporter.py
    tools/
      __init__.py
      registry.py
      search_notes.py
      read_note.py
      summarize.py
    data/
      notes.json
    runs/
      .gitkeep
```

JavaScript 版本可以参考：

```text
06-project-lab/
  README.md
  research-agent/
    main.js
    config.js
    agent.js
    state.js
    planner.js
    executor.js
    observer.js
    reporter.js
    tools/
      registry.js
      search-notes.js
      read-note.js
      summarize.js
    data/
      notes.json
    runs/
      .gitkeep
```

## 模块职责

| 模块 | 主要职责 |
| --- | --- |
| `main` | 解析输入参数，创建 Agent，启动任务 |
| `config` | 保存 `max_iterations`、日志路径等配置 |
| `agent` | 编排 `plan -> act -> observe` 主循环 |
| `state` | 保存目标、计划、观察结果、工具日志、checkpoint 和完成状态 |
| `planner` | 把研究主题拆成子任务 |
| `executor` | 根据当前步骤选择并调用工具 |
| `observer` | 把工具结果写入状态，并判断是否继续 |
| `reporter` | 生成最终研究摘要 |
| `tools/registry` | 注册工具白名单，统一工具调用入口 |

## 核心流程

```text
用户输入主题
  ↓
初始化 State
  ↓
Planner 生成计划
  ↓
进入循环，最多执行 max_iterations 次
  ↓
Executor 选择工具并执行
  ↓
Observer 记录观察结果和工具日志
  ↓
判断是否完成
  ↓
Reporter 输出研究摘要
```

主循环建议保持简单：

```text
state.plan = planner.create_plan(state.goal)

for iteration in range(config.max_iterations):
    if state.finished:
        break

    action = executor.next_action(state)
    result = tool_registry.call(action.tool_name, action.input)
    observer.record(state, iteration, action, result)
    observer.update_progress(state)

reporter.render(state)
```

## 实现步骤

### 第 1 步：准备本地资料

在 `data/notes.json` 中放入少量学习资料。示例主题可以包括：

- ReAct Agent
- MCP
- RAG
- 工具调用日志
- 最大迭代限制

注意：资料可以是教学模拟内容，不需要复制大段外部文档。

### 第 2 步：实现工具注册表

所有工具都通过 `ToolRegistry` 调用，避免 Agent 任意执行函数。

推荐接口：

```text
register(name, description, input_schema, handler)
call(name, input)
list_tools()
```

如果工具名不存在，应返回清晰错误，而不是直接抛出未处理异常。

### 第 3 步：实现 Planner

初学阶段可以使用规则方式生成计划：

```text
1. 搜索主题相关资料
2. 阅读最相关资料
3. 总结关键概念
4. 整理适合初学者的结论
```

如果后续接入大模型，必须使用环境变量读取 Key，并提供 `.env.example`，不要写入真实密钥。

### 第 4 步：实现 Executor

Executor 根据当前步骤选择工具。

示例策略：

- 第一次迭代调用 `search_notes`。
- 找到资料后调用 `read_note`。
- 资料足够后调用 `summarize`。
- 所有计划项完成后设置 `finished = true`。

### 第 5 步：实现 Observer、State 和 Tool Log

Observer 做两件事：

1. 把工具返回结果写入 `observations`。
2. 把工具调用元信息写入 `tool_logs`。

State 建议包含：

- `run_id`
- `goal`
- `plan`
- `current_step`
- `observations`
- `tool_logs`
- `decisions`
- `retry_count`
- `finished`
- `stop_reason`
- `last_error`

每轮迭代后保存 `runs/<run_id>/state.json`。如果程序重启，优先从 checkpoint 恢复，不要重复执行已经成功且有副作用的动作。

每条工具日志至少包括：

- iteration
- trace_id
- tool_name
- input
- ok
- output_preview
- error
- duration_ms
- retry_count
- next_decision

日志文件建议保存到 `runs/latest.json`。如果担心覆盖，可以用时间戳命名。

### 第 5.5 步：实现失败恢复

为每类失败定义策略：

```text
if error_type in ["timeout", "rate_limit"] and retry_count < max_retries:
    retry same action
elif error_type == "not_found":
    ask planner to revise query
elif error_type == "permission_required":
    pause for human confirmation
else:
    stop safely with stop_reason
```

恢复时要检查 checkpoint：

1. 如果 `finished=true`，只重新生成或展示报告。
2. 如果上一步工具成功但报告未生成，从 reporter 继续。
3. 如果上一步失败且可重试，从当前 step 重试。
4. 如果失败不可重试，输出当前进展和修复建议。

### 第 6 步：实现 Reporter

最终输出建议包含：

```text
# 研究摘要

## 研究主题

## 执行计划

## 关键发现

## 工具调用记录

## 未完成事项

## 下一步建议
```

当达到 `max_iterations` 仍未完成时，报告中要明确说明：

```text
由于达到最大迭代次数，本次研究提前停止。
```

## 运行方式

Python 示例：

```bash
cd lessons/05-agent/06-project-lab/research_agent
python main.py --topic "MCP 和 Agent 的关系" --max-iterations 5
```

JavaScript 示例：

```bash
cd lessons/05-agent/06-project-lab/research-agent
node main.js --topic "MCP 和 Agent 的关系" --max-iterations 5
```

## 验收方式

### 基础验收

- [ ] 可以从命令行输入研究主题。
- [ ] 可以生成不少于 3 步的计划。
- [ ] 至少调用 2 种工具。
- [ ] 每次工具调用都有日志。
- [ ] 有 `max_iterations`，且达到上限会停止。
- [ ] 工具失败时能输出错误信息并继续或安全停止。
- [ ] 最终报告结构清晰。
- [ ] 每轮迭代后保存 checkpoint。
- [ ] 支持从 checkpoint resume。
- [ ] 日志能按 `run_id` / `trace_id` 串起完整执行链路。

### 工程验收

- [ ] Agent 主循环不直接写死所有工具逻辑。
- [ ] 工具通过注册表统一管理。
- [ ] 状态对象能完整描述一次运行。
- [ ] 日志中不包含真实密钥或敏感信息。
- [ ] 代码结构能让初学者看出 Planner、Executor、Observer 的边界。

### 示例验收场景

用下面主题运行：

```text
什么是 ReAct Agent？它为什么需要工具调用日志？
```

期望看到：

1. 计划中包含“理解 ReAct”“查询工具调用日志”“总结关系”。
2. 工具日志中至少出现 `search_notes` 和 `summarize`。
3. 最终摘要能解释 `Reason + Act` 与日志可追踪性的关系。
4. 如果把 `max_iterations` 设置为 1，程序会提前停止并说明未完成事项。

## 进阶扩展

完成基础版本后，可以继续尝试：

- 加入人工确认计划步骤。
- 为工具增加风险等级。
- 把工具日志输出为 Markdown 表格。
- 增加一个简单 Evaluator 判断报告质量。
- 将本地资料替换为上一阶段 RAG 的检索结果。
