# 研究报告：Agent 如何完成研究任务

## 一句话总结
Agent 工程可以从规划、工具调用、日志记录和评测四个角度逐步理解。

## 研究计划
- 理解主题：Agent 如何完成研究任务
- 查找 Agent 基础概念
- 查找 Planner 的职责
- 查找 Tool Registry 的作用
- 查找 Eval 和安全边界

## 关键发现
- 第 1 步使用 `search_notes`：Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。
- 第 1 步使用 `summarize`：Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。
- 第 2 步使用 `search_notes`：Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。
- 第 2 步使用 `summarize`：Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。
- 第 3 步使用 `search_notes`：Planner 负责把大目标拆成可执行的小步骤，降低一次性完成任务的难度。
- 第 3 步使用 `summarize`：Planner 负责把大目标拆成可执行的小步骤，降低一次性完成任务的难度。
- 第 4 步使用 `search_notes`：Tool Registry 用来登记可调用工具，让 Agent 通过统一接口使用搜索、读取、写入等能力。
- 第 4 步使用 `summarize`：Tool Registry 用来登记可调用工具，让 Agent 通过统一接口使用搜索、读取、写入等能力。

## 适合初学者的理解方式
把 Agent 想象成一名实习研究员：先列待办，再查本地资料，每一步都写日志，最后整理报告。

## 资料来源
- 本地 notes：Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。
- 本地 notes：Planner 负责把大目标拆成可执行的小步骤，降低一次性完成任务的难度。
- 本地 notes：Tool Registry 用来登记可调用工具，让 Agent 通过统一接口使用搜索、读取、写入等能力。
- 本地 notes：agent
- 本地 notes：planner
- 本地 notes：tool

## 运行状态
- 最大迭代次数：4 次已执行
- 工具调用次数：8 次
- 是否因为 max_iterations 停止：是

## 后续学习建议
- 尝试增加网页搜索工具。
- 尝试把 Planner 替换成真实 LLM。
- 为报告质量增加 Eval。
