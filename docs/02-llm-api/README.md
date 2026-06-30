# 02 LLM API 与 SDK

## 学习目标

从使用 AI 产品进入开发 AI 应用，掌握模型 API 的基本调用方式。

## 核心概念

- API Key
- HTTP Request / Response
- Model、Messages、Temperature、Max Tokens
- Streaming 流式输出
- Token 计费
- Rate Limit
- Prompt Caching
- 多轮对话上下文管理

## 推荐学习对象

- Anthropic Claude API
- OpenAI API
- Google Gemini API
- LangChain
- LlamaIndex

## 学习任务

1. 用 Python 或 Node.js 调用一次 LLM API。
2. 实现多轮对话。
3. 实现流式输出。
4. 把 Prompt 模板接入 API。
5. 记录每次调用的输入、输出、耗时和 token 消耗。

## 实战项目

做一个 `命令行 AI 聊天助手`：

- 支持多轮对话
- 支持流式输出
- 支持选择模型
- 支持保存历史记录

## 检查标准

- 是否理解 messages 结构？
- 是否能控制输出长度和风格？
- 是否能处理 API 错误？
- 是否知道一次调用大概消耗多少 token？
