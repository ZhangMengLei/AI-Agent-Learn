# LLM API 练习

## 练习 1：理解请求结构

写出一次 LLM API 请求需要包含哪些信息。

至少包含：

- model
- messages
- temperature
- max_tokens
- stream

## 练习 2：设计 messages

为下面任务设计 messages：

```text
让 AI 扮演学习助手，用中文解释什么是 Agent。
```

要求：

- 包含 system message
- 包含 user message
- system message 要说明角色和回答风格

## 练习 3：多轮对话

构造一个三轮对话历史：

1. 用户问什么是 Prompt
2. AI 回答
3. 用户继续追问 System Prompt 是什么

思考：为什么第三次请求时需要带上前面的历史？

## 练习 4：流式输出

用伪代码描述流式输出过程：

```text
发起请求 → 接收片段 → 打印片段 → 拼接完整结果 → 保存历史
```

## 练习 5：调用日志

设计一个 JSON 日志格式，记录：

- 调用时间
- 模型名称
- 输入 token
- 输出 token
- 耗时
- 是否成功
- 错误信息

## 练习 6：成本意识

回答下面问题：

1. 为什么长上下文会增加成本？
2. 为什么流式输出不一定减少总成本？
3. Prompt Caching 适合什么场景？
4. 多轮对话为什么需要摘要或裁剪？
