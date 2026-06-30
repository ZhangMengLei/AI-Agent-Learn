# LLM API 实战项目：命令行 AI 聊天助手

## 项目目标

做一个可以在终端运行的 AI 聊天助手，理解 LLM API 在真实应用中的基本用法。

## 功能要求

### 基础功能

- 用户在命令行输入问题
- 程序调用 LLM API
- 将模型回答打印到终端
- 支持连续多轮对话

### 进阶功能

- 支持流式输出
- 支持保存对话历史
- 支持清空历史
- 支持切换模型
- 支持记录调用日志
- 支持 `mock` / `real` provider 安全切换
- 支持配置超时、重试次数和错误分类
- 支持在 streaming 中途失败时保存 partial output 并提示用户

## 推荐目录

```text
cli-chat/
  README.md
  main.py 或 main.js
  config.example.json
  logs/
  conversations/
```

## 核心流程

```text
启动程序
  ↓
读取配置和 API Key
  ↓
等待用户输入
  ↓
构造 messages
  ↓
调用模型 API
  ↓
流式打印回答
  ↓
保存对话历史
  ↓
继续等待用户输入
```

## Provider 与配置要求

项目必须保留 mock 路径，真实 API 只能作为可切换 provider 接入。

推荐配置：

```json
{
  "provider": "mock",
  "api_key_env": "ANTHROPIC_API_KEY",
  "base_url": "",
  "model": "model-name",
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": true,
  "timeout_ms": 30000,
  "max_retries": 2
}
```

要求：

- `provider=mock` 时不读取真实 Key，不访问网络。
- `provider=real` 时从 `api_key_env` 指向的环境变量读取 Key。
- 日志只记录 provider、model、latency、usage、success、error_type，不记录 Key。
- 鉴权错误、参数错误不重试；限流、超时、服务端错误可以有限重试。
- 所有真实调用前先打印当前 provider 和 model，便于确认没有误用生产配置。

## 命令设计

```text
/help       查看帮助
/clear      清空当前对话
/model      切换模型
/save       保存当前对话
/exit       退出程序
```

## 验收标准

- 可以完成一次 API 调用。
- 可以连续进行多轮对话。
- 可以流式输出。
- 不把真实 API Key 提交到仓库。
- 能记录每次调用的耗时和结果。
- mock provider 与真实 provider 使用同一套业务接口。
- 缺少 Key、鉴权失败、限流、超时、空输出都有清晰提示。
- streaming 成功时保存完整回答；中途失败时不把 partial output 当成完整成功。

## 扩展方向

- 接入 Prompt 模板库。
- 支持读取本地文件并总结。
- 支持工具调用。
- 支持 RAG 文档问答。
