# Agent 练习工程说明

本目录用于完成 05-agent 阶段的工程化练习。目标不是一次写出复杂智能体，而是用最小代码跑通 ReAct 风格的执行循环：`plan -> act -> observe`，并学会用 `max_iterations` 和工具日志控制 Agent 的可解释性与安全边界。

## 练习目标

完成后你应该能够：

1. 解释 Agent 与普通 Chatbot 的工程差异。
2. 实现一个最小 `plan-act-observe` 循环。
3. 为 Agent 设置 `max_iterations`，避免无限循环。
4. 记录每一次工具调用的输入、输出、状态和耗时。
5. 用模拟工具搭建一个“研究助手”雏形。

## 推荐目录

建议在本目录下按下面结构创建自己的练习代码：

```text
04-exercises-lab/
  README.md
  starter/
    main.py                 # 练习入口，也可以换成 main.js
    agent.py                # Agent 循环
    tools.py                # 模拟搜索、读取、摘要工具
    tool_log.py             # 工具调用日志
    prompts.py              # plan / act / observe 提示词模板
  answers/
    README.md               # 参考答案说明，不放真实密钥
```

如果你使用 JavaScript，可以将 `starter/*.py` 替换为：

```text
starter/
  main.js
  agent.js
  tools.js
  tool-log.js
  prompts.js
```

## 练习 1：最小 Plan

输入一个研究主题，例如：

```text
帮我研究“什么是 MCP，以及它适合解决什么问题”
```

要求输出 3 到 5 个子任务：

```text
1. 查询 MCP 的基础定义
2. 梳理 MCP Client / Server / Tools / Resources 的关系
3. 总结 MCP 适合的使用场景
4. 生成初学者友好的学习建议
```

初学阶段可以先不调用真实大模型，直接用规则函数或固定模板生成计划。

## 练习 2：最小 Act

实现一个工具注册表，让 Agent 只能调用白名单工具。

推荐先实现 3 个模拟工具：

| 工具名 | 作用 | 是否需要真实网络 |
| --- | --- | --- |
| `search_notes(query)` | 从本地模拟资料中检索片段 | 否 |
| `read_note(note_id)` | 读取指定资料正文 | 否 |
| `summarize(text)` | 对文本做简单摘要 | 否 |

工具函数返回统一结构：

```json
{
  "ok": true,
  "data": "工具结果",
  "error": null
}
```

失败时也要返回统一结构：

```json
{
  "ok": false,
  "data": null,
  "error": "未找到资料"
}
```

## 练习 3：Observe 与状态更新

每次工具调用后，Agent 需要把观察结果写入运行状态。

推荐状态结构：

```json
{
  "goal": "研究主题",
  "plan": ["步骤 1", "步骤 2"],
  "current_step": 0,
  "observations": [],
  "tool_logs": []
}
```

观察结果不等于最终答案。观察结果只是下一轮行动的依据。

## 练习 4：max_iterations

为主循环添加最大迭代次数：

```text
for i in range(max_iterations):
    plan_or_select_next_step()
    act()
    observe()
    if is_finished():
        break
```

验收要求：

- 默认 `max_iterations = 5`。
- 达到上限后必须停止。
- 停止时输出当前已完成内容和未完成内容。
- 不允许用无限 `while True` 且没有退出条件。

## 练习 5：工具调用日志

为每一次工具调用记录日志。推荐字段：

```json
{
  "iteration": 1,
  "tool_name": "search_notes",
  "input": {"query": "MCP 基础定义"},
  "ok": true,
  "output_preview": "MCP 是 Model Context Protocol...",
  "error": null,
  "duration_ms": 12
}
```

日志可以先打印到终端，也可以写入本地 JSON 文件。注意不要记录真实 API Key、Cookie、Token 等敏感信息。

## 运行方式

Python 示例：

```bash
cd lessons/05-agent/04-exercises-lab/starter
python main.py --topic "什么是 MCP" --max-iterations 5
```

JavaScript 示例：

```bash
cd lessons/05-agent/04-exercises-lab/starter
node main.js --topic "什么是 MCP" --max-iterations 5
```

如果你还没有实现命令行参数，也可以先在 `main.py` 或 `main.js` 中写死一个测试主题。

## 参考答案说明

参考答案建议放在 `answers/` 目录下，但练习时不要先看答案。

参考答案应包含：

1. 一个可以运行的最小 ReAct Agent。
2. 至少 3 个模拟工具。
3. `max_iterations` 保护。
4. 完整工具调用日志。
5. 一份示例运行输出。

参考答案不应包含：

- 真实 API Key。
- 对外部付费 API 的强依赖。
- 难以理解的大型框架封装。

## 自检清单

- [ ] 我能说清楚 Plan、Act、Observe 分别对应哪段代码。
- [ ] Agent 不会无限循环。
- [ ] 工具只能从白名单中选择。
- [ ] 每次工具调用都有日志。
- [ ] 工具失败时不会导致程序崩溃。
- [ ] 最终输出能说明“已完成什么、还缺什么”。
