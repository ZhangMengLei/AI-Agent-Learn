# LLM API 练习工程说明

本目录用于完成 LLM API 与 SDK 阶段的练习实验。目标不是直接做完整应用，而是分步骤理解一次模型调用从“配置、请求、响应、错误处理、日志记录”到“多轮对话”的完整过程。

注意：本阶段会涉及 API Key，但不要把真实 API Key 写入代码、README 或提交到仓库。示例中只能使用占位符，例如 `YOUR_API_KEY` 或从环境变量读取。

## 练习目标

完成本实验后，你应该能够：

1. 说明一次 LLM API 请求的基本结构。
2. 正确组织 `messages`。
3. 理解多轮对话为什么需要携带上下文。
4. 理解流式输出的基本流程。
5. 设计调用日志，记录耗时、模型、token 和错误。
6. 知道如何保护 API Key。

## 推荐目录

建议在本目录下按下面结构组织练习：

```text
04-exercises-lab/
  README.md
  exercise-01-request-structure.md
  exercise-02-messages.md
  exercise-03-multi-turn.md
  exercise-04-streaming.md
  exercise-05-logging.md
  exercise-06-cost.md
  answers/
    exercise-01-reference.md
    exercise-02-reference.md
    exercise-03-reference.md
```

如果你选择写代码练习，也可以使用下面结构：

```text
04-exercises-lab/
  README.md
  python/
    request_demo.py
    streaming_demo.py
  node/
    request_demo.js
    streaming_demo.js
```

代码语言不限。初学者建议先用伪代码和 JSON 理解结构，再写真实代码。

## 环境准备建议

不要在代码中硬编码真实 Key。建议使用环境变量：

```bash
export LLM_API_KEY="YOUR_API_KEY"
```

在代码或伪代码中读取：

```text
api_key = read_env("LLM_API_KEY")
```

如果使用配置文件，请只保留示例文件：

```text
config.example.json
```

示例内容：

```json
{
  "api_key_env": "LLM_API_KEY",
  "model": "your-model-name",
  "base_url": "https://api.example.com"
}
```

## 练习 1：理解请求结构

### 任务

写出一次 LLM API 请求通常包含哪些字段，并说明作用。

至少包含：

- `model`：选择哪个模型。
- `messages`：对话内容。
- `temperature`：控制随机性。
- `max_tokens`：限制最大输出长度。
- `stream`：是否使用流式输出。

### 输出模板

```text
字段名：
作用：
常见取值：
初学者注意事项：
```

## 练习 2：设计 messages

### 任务

为下面任务设计 `messages`：

```text
让 AI 扮演学习助手，用中文解释什么是 Agent。
```

### 要求

- 至少包含一条 system message。
- 至少包含一条 user message。
- system message 要定义角色、回答风格和边界。
- user message 要表达具体问题。

### 参考结构

```json
[
  {
    "role": "system",
    "content": "你是一个适合初学者的 AI 学习助手，用中文回答，尽量用类比解释。"
  },
  {
    "role": "user",
    "content": "请解释什么是 Agent，并给一个生活中的类比。"
  }
]
```

## 练习 3：多轮对话上下文

### 任务

构造一个三轮对话历史：

1. 用户问：什么是 Prompt？
2. AI 回答：Prompt 是给模型的任务说明。
3. 用户追问：那 System Prompt 是什么？

### 思考问题

- 如果第三轮请求不带前两轮历史，模型还能理解“那”指什么吗？
- 多轮历史越长越好吗？
- 什么时候应该裁剪历史或做摘要？

### 推荐记录方式

```json
[
  { "role": "user", "content": "什么是 Prompt？" },
  { "role": "assistant", "content": "Prompt 是给模型的任务说明。" },
  { "role": "user", "content": "那 System Prompt 是什么？" }
]
```

## 练习 4：流式输出流程

### 任务

用伪代码描述流式输出过程。

### 参考流程

```text
发起 stream 请求
创建 full_text = ""
循环读取模型返回的 chunk
  如果 chunk 中有文本片段
    打印片段，不换行
    追加到 full_text
请求结束后
  把 full_text 保存到 messages
  记录日志
```

### 思考问题

- 流式输出主要改善什么体验？
- 流式输出是否一定更省钱？
- 如果中途断开，应该如何处理已经收到的文本？

## 练习 5：调用日志设计

### 任务

设计一个 JSON 日志格式，用来记录每次 API 调用。

### 推荐字段

```json
{
  "request_id": "",
  "started_at": "",
  "ended_at": "",
  "latency_ms": 0,
  "model": "",
  "input_tokens": 0,
  "output_tokens": 0,
  "stream": false,
  "success": true,
  "error_type": null,
  "error_message": null
}
```

### 注意事项

- 日志中不要记录 API Key。
- 如果保存用户输入，要考虑隐私信息。
- 错误日志要足够帮助排查问题。

## 练习 6：成本与限流意识

### 任务

回答下面问题：

1. 为什么长上下文会增加成本？
2. 为什么流式输出不一定减少总成本？
3. 为什么需要设置 `max_tokens`？
4. 遇到 Rate Limit 应该如何处理？
5. Prompt Caching 适合哪些重复上下文较多的场景？

## 参考答案说明

参考答案主要用于检查思路，不是唯一标准。你自己的答案只要满足以下条件，也可以认为合格：

- 字段含义解释正确。
- `messages` 角色清晰。
- 多轮对话能体现上下文关系。
- 流式输出流程完整。
- 日志不包含敏感信息。
- 对成本和限流有基本意识。

## 完成标准

完成本实验至少需要：

- 写出一次 API 请求结构说明。
- 写出 2 组不同任务的 `messages`。
- 写出一个三轮对话历史。
- 写出流式输出伪代码。
- 设计一份调用日志 JSON。
- 说明如何避免泄露 API Key。
