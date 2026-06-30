# MCP 常用模板

本文件提供 MCP Server 从协议、能力设计到客户端配置的常用模板。示例均使用占位路径和占位环境变量，不包含真实密钥。

## MCP Server 项目结构模板

```text
my-mcp-server/
  README.md
  package.json 或 pyproject.toml
  config.example.json
  src/
    server.ts 或 server.py          # Server 入口，负责初始化与注册能力
    config.ts 或 config.py          # 读取和校验配置
    types.ts 或 types.py            # 公共类型
    tools/                          # 可执行动作
    resources/                      # 只读上下文
    prompts/                        # 可复用提示词模板
    utils/
      errors.ts 或 errors.py        # 统一错误
      logger.ts 或 logger.py        # 日志写 stderr 或文件
  data/                             # 本地演示数据
```

## 生命周期处理模板

Server 入口建议按这个顺序组织：

```text
1. 读取命令行参数，例如 --config config.example.json。
2. 加载配置，校验 dataDir、权限、启用能力列表。
3. 创建 MCP Server 实例，声明 name/version/capabilities。
4. 注册 enabledTools 中允许的工具。
5. 注册 enabledResources 中允许的资源。
6. 注册 enabledPrompts 中允许的提示词。
7. 选择传输方式，初学项目优先 stdio。
8. 启动监听，等待 Client initialize。
9. 每次请求都做 schema 校验、权限校验、错误转换和日志记录。
10. 连接关闭时释放文件句柄、网络连接等资源。
```

## JSON-RPC 消息模板

MCP 消息是 JSON-RPC 2.0 风格。下面是教学用抽象示例：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "clientInfo": {
      "name": "example-client",
      "version": "0.1.0"
    }
  }
}
```

成功响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "serverInfo": {
      "name": "learning-notes-mcp",
      "version": "0.1.0"
    }
  }
}
```

错误响应：

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

## Tool 定义模板

```json
{
  "name": "query_user_profile",
  "description": "根据用户 ID 查询用户基础资料，只返回非敏感字段。不要用于查询手机号、证件号、Token 等敏感信息。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "minLength": 1,
        "description": "用户 ID，不能为空"
      }
    },
    "required": ["user_id"],
    "additionalProperties": false
  }
}
```

设计要点：

- 名称用动词开头，例如 `search_notes`、`get_note`。
- description 同时写“能做什么”和“不能做什么”。
- schema 要限制类型、必填字段、枚举、长度和额外字段。
- 读操作和写操作分开设计，不要用一个大而全的 Tool。

## Tool 返回模板

MCP Tool 返回通常包含 `content`。文本结果可这样组织：

```json
{
  "content": [
    {
      "type": "text",
      "text": "用户昵称：Alice\n用户等级：VIP"
    }
  ]
}
```

如果返回结构化数据，可以先序列化成稳定 JSON 文本：

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"matches\":[{\"note_id\":\"mcp-basic\",\"title\":\"MCP 基础\"}]}"
    }
  ]
}
```

## Resource 定义模板

```json
{
  "uri": "docs://agent/intro",
  "name": "Agent 入门文档",
  "description": "介绍 Agent 基础概念的文档",
  "mimeType": "text/markdown"
}
```

Resource 内容返回模板：

```json
{
  "contents": [
    {
      "uri": "docs://agent/intro",
      "mimeType": "text/markdown",
      "text": "# Agent 入门\nAgent 是围绕目标持续执行的系统..."
    }
  ]
}
```

Resource 设计要点：

- URI 稳定，例如 `notes://mcp/basic`。
- 不直接暴露本地路径，例如不要让客户端读取 `/Users/name/.ssh/id_rsa`。
- Resource 只读，不承担删除、更新、发送等动作。

## Prompt 定义模板

```json
{
  "name": "review_code",
  "description": "对代码变更进行审查，输出风险、建议和测试点。",
  "arguments": [
    {
      "name": "diff",
      "description": "代码 diff 内容",
      "required": true
    },
    {
      "name": "focus",
      "description": "审查重点，例如 security、performance、readability",
      "required": false
    }
  ]
}
```

Prompt 内容模板：

```text
你是一名代码审查助手。请审查下面 diff。

审查重点：{{focus}}
代码 diff：{{diff}}

请输出：
1. 必须修复的问题
2. 建议优化的问题
3. 需要补充的测试
```

## 错误处理模板

建议在 Server 内统一把业务异常转换为协议错误或稳定 Tool 结果：

```json
{
  "error": {
    "type": "INVALID_PARAMS",
    "message": "query 不能为空",
    "hint": "请传入至少 1 个字符的搜索关键词"
  }
}
```

错误分类建议：

| 错误类型 | 使用场景 | 对外信息 |
| --- | --- | --- |
| `INVALID_PARAMS` | 参数缺失、类型错误、为空 | 指出哪个参数不合法 |
| `NOT_FOUND` | 笔记、资源、模板不存在 | 指出资源不存在，不泄露路径 |
| `PERMISSION_DENIED` | 只读模式下写入、越权访问 | 说明权限不足 |
| `UPSTREAM_ERROR` | 外部服务失败 | 说明依赖暂不可用 |
| `INTERNAL_ERROR` | 未预期异常 | 对外简短，细节写安全日志 |

## stdio Server 配置模板

stdio 适合本地 MCP Server。注意 stdout 只写协议消息，日志写 stderr。

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/my-mcp-server/dist/server.js", "--config", "/ABSOLUTE/PATH/my-mcp-server/config.example.json"],
      "cwd": "/ABSOLUTE/PATH/my-mcp-server",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

Python 示例：

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/learning_notes_mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

## SSE Server 概念模板

SSE 适合远端 Server。教学阶段只需要理解配置通常会包含服务地址和认证方式，真实项目要严格鉴权。

```json
{
  "mcpServers": {
    "remote-docs": {
      "url": "https://example.internal.invalid/mcp/sse",
      "headers": {
        "Authorization": "Bearer ${MCP_DOCS_TOKEN}"
      }
    }
  }
}
```

注意：

- 上面的 URL 是占位示例，不是可用服务。
- 不要在配置文件中写真实 Token。
- 远端 Server 必须使用 HTTPS、认证、授权、限流和审计。

## Claude Desktop 配置示例

Claude Desktop 的配置文件位置因系统不同而不同。教学时重点是配置内容：

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

## Claude Code 配置示例

Claude Code 的具体配置入口可能随版本变化。无论通过命令行还是配置文件添加，本质都要提供同样信息：

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

配置后检查：

- Server 名称是否唯一。
- `command` 在客户端环境中是否可执行。
- `args` 中的路径是否存在。
- `cwd` 是否为项目目录。
- 所需环境变量是否已在本机安全配置，不要提交真实值。

## 权限设计模板

```text
工具名称：update_ticket
风险等级：中
能力：修改工单状态
默认状态：禁用
权限策略：执行前展示修改内容，并要求用户确认
审计日志：记录操作者、时间、参数摘要、结果
敏感信息：不记录 Token、Cookie、完整用户隐私字段
失败处理：权限不足时返回 PERMISSION_DENIED
```

## MCP Server 检查清单

- [ ] Server 生命周期是否清晰：启动、initialize、注册、调用、关闭。
- [ ] Tool 名称是否清晰？
- [ ] 输入 schema 是否准确且足够严格？
- [ ] 返回格式是否稳定？
- [ ] Resource 是否使用稳定 URI？
- [ ] Prompt 参数是否清晰？
- [ ] 是否过滤敏感字段？
- [ ] 写操作是否默认禁用或需要确认？
- [ ] 错误信息是否可理解？
- [ ] stdout 是否只输出协议消息？
- [ ] 配置示例是否不包含真实密钥？
