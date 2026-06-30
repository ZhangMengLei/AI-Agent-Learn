# LLM API 项目实现工程说明：CLI Chatbot

本项目实验要求你设计并实现一个命令行 AI 聊天助手。它是从“会调用一次 API”走向“能做一个小型 AI 应用”的关键练习。

注意：不要在任何文件中写入真实 API Key。请使用环境变量或本地配置文件，并把配置示例和真实配置分开。

## 项目目标

实现一个可以在终端运行的 CLI Chatbot，支持：

1. 用户输入问题。
2. 程序构造 `messages`。
3. 调用 LLM API。
4. 输出模型回答。
5. 支持连续多轮对话。
6. 支持基础命令，例如退出、清空上下文、查看帮助。
7. 记录调用日志。

完成后，你应该理解一个 LLM 应用的最小闭环：输入、上下文、请求、响应、日志、错误处理。

## 推荐文件结构

可以选择 Python 或 Node.js。下面以通用结构表示：

```text
06-project-lab/
  README.md
  cli-chatbot/
    README.md
    config.example.json
    .gitignore
    src/
      main.py 或 main.js
      client.py 或 client.js
      conversation.py 或 conversation.js
      commands.py 或 commands.js
      logger.py 或 logger.js
    conversations/
      .gitkeep
    logs/
      .gitkeep
```

说明：

- `main`：程序入口，负责命令行交互循环。
- `client`：封装 LLM API 调用。
- `conversation`：管理多轮对话上下文。
- `commands`：处理 `/help`、`/clear`、`/exit` 等命令。
- `logger`：记录调用日志。
- `config.example.json`：配置示例，不包含真实 Key。
- `logs/`：保存调用日志。
- `conversations/`：保存对话历史。

如果是初学者，也可以先把所有逻辑写在一个文件中，跑通后再拆分模块。

## 配置设计

### 环境变量

推荐从环境变量读取 API Key：

```bash
export LLM_API_KEY="YOUR_API_KEY"
```

### 配置示例

`config.example.json` 可以设计为：

```json
{
  "api_key_env": "LLM_API_KEY",
  "base_url": "https://api.example.com",
  "model": "your-model-name",
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": true
}
```

不要创建包含真实 Key 的 `config.json` 示例。如果本地需要使用真实配置，请确保它不会被提交。

## 功能设计

### 1. 启动程序

启动后显示欢迎语和基础命令：

```text
AI Chatbot 已启动。输入 /help 查看命令，输入 /exit 退出。
```

### 2. 用户输入循环

程序持续读取用户输入：

```text
You> 什么是 Prompt？
AI> Prompt 是你给模型的任务说明……
```

### 3. 多轮对话

每次用户输入都追加到 `messages`：

```json
{ "role": "user", "content": "用户输入" }
```

模型回答后追加：

```json
{ "role": "assistant", "content": "模型回答" }
```

下一次请求时带上历史上下文。

### 4. 系统提示词

建议程序启动时加入一条 system message：

```text
你是一个适合初学者的 AI 学习助手。请用中文回答，解释概念时给出简单例子。如果信息不确定，请明确说明。
```

### 5. 基础命令

建议支持：

```text
/help       查看帮助
/clear      清空当前对话历史，但保留 system message
/save       保存当前对话到 conversations 目录
/history    显示当前对话轮数
/model      查看或切换模型
/exit       退出程序
```

初学者可以先实现 `/help`、`/clear`、`/exit`，再实现其他命令。

### 6. 流式输出

如果 API 支持 stream，推荐实现流式打印：

```text
收到一个文本片段 → 立即打印 → 追加到完整回答 → 请求结束后保存完整回答
```

如果暂时不会实现流式输出，可以先实现普通输出，再把 stream 作为进阶任务。

### 7. 错误处理

至少处理以下情况：

- 没有配置 API Key。
- 网络请求失败。
- API 返回鉴权错误。
- API 返回限流错误。
- 模型输出为空。
- 用户输入为空。

错误提示要对初学者友好，例如：

```text
未检测到 LLM_API_KEY，请先设置环境变量后再运行。
```

### 8. 日志记录

每次调用建议记录一行 JSON：

```json
{
  "request_id": "20260630-001",
  "started_at": "2026-06-30T10:00:00Z",
  "latency_ms": 1200,
  "model": "your-model-name",
  "input_tokens": 0,
  "output_tokens": 0,
  "stream": true,
  "success": true,
  "error_type": null,
  "error_message": null
}
```

日志中不要记录 API Key。是否记录用户原文，要根据隐私要求决定。

## 推荐实现步骤

### 第 1 步：搭建最小程序

实现一个命令行循环：

```text
读取用户输入
如果输入 /exit，退出
否则打印一条固定回复
```

目标：先跑通交互，不急着接 API。

### 第 2 步：读取配置

实现：

- 读取环境变量 `LLM_API_KEY`。
- 读取模型名、温度、最大输出长度等配置。
- 如果缺少 Key，给出清晰错误提示。

### 第 3 步：完成一次 API 调用

先实现非流式调用：

```text
用户输入 → 构造 messages → 调用 API → 打印完整回答
```

目标：确保最小闭环可用。

### 第 4 步：支持多轮对话

把用户输入和模型输出都保存到内存中的 `messages`。下一次请求时带上历史。

注意：历史过长会增加成本，后续可以加入裁剪策略。

### 第 5 步：实现基础命令

优先实现：

- `/help`
- `/clear`
- `/exit`

再实现：

- `/save`
- `/history`
- `/model`

### 第 6 步：支持流式输出

把完整回答改成边接收边打印。请求结束后，仍然要保存完整文本到对话历史。

### 第 7 步：增加日志

记录每次调用：

- 开始时间。
- 结束时间或耗时。
- 模型名。
- 是否成功。
- 错误信息。
- token 用量，如果 API 返回。

### 第 8 步：整理 README

在项目 README 中写清楚：

- 如何安装依赖。
- 如何配置环境变量。
- 如何启动。
- 支持哪些命令。
- 不要提交真实 API Key。

## 验收方式

### 基础验收

必须满足：

- 程序可以启动。
- 用户可以输入问题并得到模型回答。
- 支持 `/exit` 退出。
- 真实 API Key 没有写入代码或文档。
- 至少完成一次成功调用。

### 标准验收

建议满足：

- 支持多轮对话。
- 支持 `/help` 和 `/clear`。
- 有清晰错误提示。
- 有调用日志。
- 配置示例不包含真实 Key。

### 进阶验收

可以挑战：

- 支持流式输出。
- 支持保存和加载对话历史。
- 支持切换模型。
- 支持上下文裁剪或摘要。
- 支持接入上一阶段的 Prompt 模板库。

## 测试建议

至少测试下面场景：

1. 正常提问：输入一个概念问题，检查是否能回答。
2. 多轮追问：第二轮使用“它”“上面那个”等指代词，检查上下文是否生效。
3. 清空上下文：执行 `/clear` 后再追问，检查历史是否被清空。
4. 缺少 Key：移除环境变量，检查错误提示是否清晰。
5. 退出程序：输入 `/exit`，检查是否正常结束。
6. 空输入：直接回车，检查程序是否忽略或提示。

## 安全提醒

- 不要提交真实 API Key。
- 不要在日志中记录 API Key。
- 不要把包含隐私信息的对话记录公开。
- 如果要分享项目，只分享 `config.example.json`。
- 如果 API 报错，不要把完整请求头贴到公开环境。

## 扩展方向

完成 CLI Chatbot 后，可以继续扩展：

1. 接入 Prompt 模板库。
2. 增加对话摘要，降低长上下文成本。
3. 增加文件读取，总结本地文档。
4. 增加工具调用能力。
5. 增加 RAG 文档问答能力。
