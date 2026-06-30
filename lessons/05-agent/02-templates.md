# Agent 常用模板

## Agent Loop 模板

```text
输入目标 goal
初始化 steps = []
初始化 iteration = 0
设置 max_iterations = 10

while iteration < max_iterations:
  1. 基于 goal 和当前观察生成下一步计划
  2. 判断是否已经完成
  3. 如果完成，输出最终结果并停止
  4. 如果未完成，选择一个动作
  5. 如果动作需要工具，检查权限
  6. 执行动作
  7. 记录观察结果
  8. 更新 steps
  9. iteration += 1

如果超过最大次数：
  输出当前进展和未完成原因
```

## 任务记录模板

```json
{
  "goal": "研究 MCP 是什么并写一份入门总结",
  "status": "running",
  "steps": [
    {
      "step": 1,
      "thought": "需要先理解 MCP 的定义和组成部分",
      "action": "search_docs",
      "observation": "找到 MCP Client、Server、Tools、Resources 等概念",
      "status": "completed"
    }
  ]
}
```

## 工具调用记录模板

```json
{
  "iteration": 2,
  "tool_name": "search_docs",
  "arguments": {
    "query": "MCP Client Server Tools Resources"
  },
  "permission": "auto_allowed",
  "result_summary": "检索到 MCP 核心概念",
  "error": null
}
```

## 终止条件模板

Agent 必须有明确终止条件：

```text
满足以下任一条件时停止：
1. 目标已经完成
2. 达到最大迭代次数
3. 连续 3 次没有新信息
4. 用户取消任务
5. 需要高风险权限但用户拒绝
6. 工具持续失败，无法继续推进
```

## Planner Prompt 模板

```text
你是任务规划器。

请把用户目标拆成可执行步骤。

要求：
1. 每一步都要具体
2. 每一步最多调用一个工具
3. 标出哪些步骤需要用户确认
4. 不要执行，只输出计划

用户目标：
{{goal}}
```

## Executor Prompt 模板

```text
你是任务执行器。

请根据当前目标、计划和已有观察，执行下一步。

目标：
{{goal}}

计划：
{{plan}}

已有观察：
{{observations}}

可用工具：
{{tools}}

要求：
1. 只执行下一步
2. 如果需要工具，输出工具名称和参数
3. 如果已经完成，输出 final_answer
```

## Evaluator Prompt 模板

```text
你是任务评估器。

请判断当前结果是否已经满足用户目标。

用户目标：
{{goal}}

当前结果：
{{result}}

请输出：
- 是否完成：是/否
- 缺少什么
- 下一步建议
```
