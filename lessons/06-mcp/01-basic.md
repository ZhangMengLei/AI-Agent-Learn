# MCP 基础

## MCP 是什么

MCP 是 Model Context Protocol，可以理解为 AI 应用连接工具、数据源和提示词模板的一套标准协议。它让 Claude Code、Claude Desktop、IDE 插件或你自己的 Agent 应用，用同一种方式发现和调用外部能力。

它解决的问题是：不同 AI 客户端都需要访问文件、数据库、GitHub、内部系统，如果每个客户端都单独开发一套插件，会非常混乱。MCP 提供了一种统一方式，让能力由 MCP Server 暴露，AI 客户端通过 MCP Client 使用。

## 基本角色

### MCP Client

MCP Client 是使用 MCP Server 能力的一方，通常嵌在 AI 应用内部。

例如：

- Claude Code
- Claude Desktop
- IDE 插件
- 自己开发的 Agent 应用

Client 负责：

1. 启动或连接 MCP Server。
2. 完成初始化握手。
3. 发现 Server 暴露的 tools、resources、prompts。
4. 在模型需要时发起调用。
5. 将调用结果安全地交给模型继续推理。

### MCP Server

MCP Server 是提供工具、资源或提示词的一方。

例如：

- 文件系统 Server
- GitHub Server
- 数据库 Server
- 浏览器 Server
- 内部业务系统 Server
- 课程知识库 Server

Server 负责：

1. 声明自身名称、版本和能力。
2. 注册 tools、resources、prompts。
3. 校验输入参数。
4. 执行受控操作或读取受控上下文。
5. 返回结构化结果或结构化错误。

## Client/Server 生命周期

一个典型 MCP 会话可以按下面顺序理解：

```text
1. Client 根据配置启动 Server，或连接远端 Server。
2. Client 与 Server 建立传输通道，例如 stdio 或 SSE。
3. Client 发送 initialize 请求，包含客户端信息和能力声明。
4. Server 返回协议版本、服务端信息和能力声明。
5. Client 发送 initialized 通知，表示初始化完成。
6. Client 按需调用 listTools/listResources/listPrompts 发现能力。
7. 模型需要外部能力时，Client 发送 callTool/readResource/getPrompt 等请求。
8. Server 校验权限和参数，执行逻辑，返回结果。
9. 会话结束时，Client 关闭连接，Server 释放资源并退出。
```

生命周期中最容易出错的点：

- Server 启动命令、工作目录或参数写错。
- initialize 阶段协议版本或能力声明不匹配。
- Tool schema 不准确，导致 Client 生成错误参数。
- Server 将业务异常当作进程崩溃处理，导致 Client 只能看到连接中断。
- 日志写到 stdout 干扰 stdio 协议数据。

## MCP 能提供什么

### Tools

Tools 是可执行动作。

例如：

- 查询数据库
- 搜索本地 Markdown 文档
- 读取指定笔记
- 创建工单
- 调用内部 API

Tools 通常会改变或查询外部世界，所以需要关注权限。每个 Tool 至少要有：

- `name`：稳定、简短、可读。
- `description`：说明何时使用、何时不要使用。
- `inputSchema`：JSON Schema，描述参数类型、必填字段和限制。
- 输出格式：成功与失败都要稳定。

### Resources

Resources 是可读取资源，更偏“上下文读取”。

例如：

- 某个文件内容
- 某张数据库表结构
- 某个接口文档
- 某个项目配置
- 某个课程章节

Resource 应该使用稳定 URI，而不是把任意本地路径暴露给客户端。例如：

```text
notes://mcp/basic
course://06-mcp/review
```

### Prompts

Prompts 是可复用的提示词模板。

例如：

- 代码审查模板
- PR 总结模板
- 安全检查模板
- 故障排查模板
- 学习复盘模板

Prompt 不负责执行外部动作，而是把一类任务沉淀成可复用输入模板。它应声明参数，例如 `topic`、`notes`、`level`。

### Sampling

Sampling 是 MCP Server 请求模型生成内容的能力。它让 Server 在某些场景下也可以借助模型能力，但实际使用时要非常注意权限和边界。初学项目可以先不实现 Sampling。

## JSON-RPC

MCP 底层消息采用 JSON-RPC 2.0 风格。你可以先简单理解为：

```text
客户端发送结构化请求，服务端返回结构化响应。
```

请求通常包含：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_notes",
    "arguments": {
      "query": "MCP"
    }
  }
}
```

成功响应通常包含：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "找到 2 条笔记"
      }
    ]
  }
}
```

错误响应通常包含：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params: query is required"
  }
}
```

学习重点不是背错误码，而是理解：请求、响应、错误都要结构化，Client 才能稳定处理。

## stdio 与 SSE

MCP 可以跑在不同传输方式上。初学最常见的是 stdio。

### stdio

stdio 指 Client 启动一个本地 Server 进程，通过标准输入和标准输出交换 JSON-RPC 消息。

适合：

- 本地开发。
- 访问本地文件或本地课程资料。
- Claude Desktop / Claude Code 本地 Server 配置。

注意：

- stdout 必须只输出协议消息。
- 普通日志应写 stderr 或日志文件。
- 启动命令、参数、工作目录要配置准确。

### SSE

SSE 是 Server-Sent Events，常用于连接远端或长连接服务。Client 通过 HTTP 连接接收服务端事件，再配合请求通道完成通信。

适合：

- 远端托管 MCP Server。
- 多客户端共享服务。
- 需要集中鉴权、审计、限流的场景。

注意：

- 要使用 HTTPS。
- 要有认证、授权和限流。
- 不要把内部服务裸露到公网。

## Schema 设计

Tool 的输入 schema 是 Client 正确调用的基础。一个好的 schema 应该：

- 使用明确类型：`string`、`number`、`boolean`、`array`、`object`。
- 写清必填字段：`required`。
- 对枚举值使用 `enum`。
- 对字符串长度、数组长度、数字范围设置限制。
- 在 description 中说明边界，而不是只重复字段名。

示例：

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1,
      "description": "搜索关键词，不能为空"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "description": "最多返回条数，默认 5"
    }
  },
  "required": ["query"]
}
```

## 错误处理

MCP Server 不应该把所有失败都变成“程序崩溃”。建议区分：

| 类型 | 示例 | 返回建议 |
| --- | --- | --- |
| 参数错误 | query 为空 | `Invalid params: query is required` |
| 未找到 | note_id 不存在 | `Not found: note mcp-basic` |
| 权限不足 | 尝试写入只读 Server | `Permission denied: read-only mode` |
| 外部依赖失败 | 数据库不可用 | `Upstream unavailable: database` |
| 内部错误 | 未预期异常 | `Internal error`，日志记录细节 |

对外错误信息要清楚但不要泄露敏感细节；内部日志可以记录更多上下文，但不能记录 Token、Cookie、密钥和完整敏感数据。

## 调试方法

调试 MCP Server 时建议按层排查：

1. 先直接运行启动命令，确认进程能启动。
2. 检查配置文件路径、工作目录和环境变量。
3. 使用最小输入调用一个只读 Tool。
4. 验证 listTools/listResources/listPrompts 是否能列出能力。
5. 检查 stderr 或日志文件，不要在 stdout 打印调试文本。
6. 给参数错误、未找到、权限不足各写一个测试样例。

常见现象：

- 客户端看不到 Server：启动命令或路径错误。
- 调用后卡住：Server 没有按 JSON-RPC 返回，或 stdout 被日志污染。
- 模型总是传错参数：schema 太宽泛或 description 不清楚。
- 本地能跑、客户端不能跑：客户端工作目录和 shell 环境不同。

## 客户端配置示例

### Claude Desktop 示例

示例路径因系统不同而不同。下面只展示配置结构，不包含真实密钥：

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": [
        "-m",
        "src.server",
        "--config",
        "/ABSOLUTE/PATH/lessons/06-mcp/06-project-lab/learning_notes_mcp/config.example.json"
      ],
      "cwd": "/ABSOLUTE/PATH/lessons/06-mcp/06-project-lab/learning_notes_mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

### Claude Code 示例

Claude Code 也可以配置本地 MCP Server。配置方式可能随版本变化，核心仍然是提供 server 名称、启动命令、参数、工作目录和必要环境变量。

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/lessons/06-mcp/06-project-lab/learning_notes_mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

配置原则：

- 使用绝对路径，减少工作目录差异。
- 示例中只放占位值，不放真实 API Key。
- 本地私有配置不要提交到仓库。
- 如果需要密钥，优先从环境变量读取。

## 权限与安全

MCP Server 连接真实系统，因此必须注意：

- 哪些工具可读？
- 哪些工具可写？
- 哪些操作需要用户确认？
- 是否会泄露敏感数据？
- 工具返回内容是否可信？

最低安全基线：

1. 默认只读，写操作显式开启。
2. 不允许读取任意本地路径，只允许受控目录或固定 URI。
3. 不在仓库、配置示例、日志中写真实密钥。
4. 对工具参数做 schema 校验和业务校验。
5. 对写操作增加确认、审计日志和最小权限账户。
6. 对远端 SSE Server 增加认证、授权、HTTPS 和限流。
7. 工具返回内容当作不可信输入，避免把外部文本直接当指令执行。

## MCP 解决什么问题

- 工具接入标准化。
- 数据源暴露标准化。
- 工具可以被多个 AI 客户端复用。
- 企业内部能力可以封装为 MCP Server。
- Agent 不需要知道每个系统的私有接入细节。

## 一句话总结

MCP 是让 AI Agent 标准化使用外部工具、上下文和提示词模板的协议；学 MCP 不只是学“怎么调用工具”，更要学生命周期、协议消息、schema、错误处理、调试和权限边界。
