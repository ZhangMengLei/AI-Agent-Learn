# MCP 练习工程说明

本目录用于完成 06-mcp 阶段的工程化练习。目标是理解一个自定义 MCP Server 应该如何设计，而不是一开始就接入复杂外部系统。请先用本地数据实现最小 Server，再逐步补充 tools、resources、prompts、config、错误处理和客户端配置。

建议使用 stdio 作为第一个传输方式，因为它最适合本地学习和 Claude Desktop / Claude Code 本地集成。SSE 只需要先理解概念和安全要求，不要求在本练习中实现。

## 练习目标

完成后你应该能够：

1. 说明 MCP Client 与 MCP Server 的关系。
2. 说明一个 MCP 会话从启动、initialize、能力发现、调用到关闭的生命周期。
3. 区分 Tools、Resources、Prompts 的职责。
4. 设计一个最小 MCP Server 的目录结构。
5. 为工具定义输入 schema 和清晰错误返回。
6. 使用配置文件描述 Server 名称、数据目录、启用的工具和权限边界。
7. 写出 Claude Desktop / Claude Code 的本地配置示例。
8. 解释 stdio 调试要点和 SSE 安全要点。

## 推荐目录

建议在本目录下按下面结构组织练习代码：

```text
04-exercises-lab/
  README.md
  starter/
    server.py 或 server.ts       # MCP Server 入口
    config.example.json          # 示例配置，不写真实密钥
    tools/
      search_notes.py 或 searchNotes.ts
      get_note.py 或 getNote.ts
    resources/
      notes.py 或 notes.ts
    prompts/
      review.py 或 review.ts
    data/
      notes.json
    utils/
      errors.py 或 errors.ts
      logger.py 或 logger.ts
  answers/
    README.md                    # 参考答案说明
```

说明：

- `tools/` 放可执行动作。
- `resources/` 放可读取上下文。
- `prompts/` 放可复用提示词模板。
- `utils/errors` 统一参数错误、未找到、权限不足、内部错误。
- `utils/logger` 的日志应写 stderr 或文件，不要污染 stdout。
- `config.example.json` 放示例配置，不放真实 Token、Cookie 或 API Key。

## 练习 1：设计 Server 信息

先写出 MCP Server 的基本信息：

```json
{
  "name": "learning-notes-mcp",
  "description": "为 AI 客户端提供学习笔记搜索、读取和复盘提示词",
  "version": "0.1.0"
}
```

思考：这个 Server 是给谁用的？提供什么能力？不提供什么能力？

建议明确写出边界：

- 提供：本地学习笔记搜索、固定资源读取、学习复盘 Prompt。
- 不提供：任意文件读取、删除文件、提交代码、调用真实内部 API。

## 练习 2：写出生命周期

请在 `starter/README.md` 或代码注释中写出你的 Server 生命周期：

```text
Client 读取配置
  -> 通过 command/args/cwd 启动 Server
  -> stdio 建立 JSON-RPC 通道
  -> initialize
  -> initialized
  -> tools/list、resources/list、prompts/list
  -> tools/call、resources/read、prompts/get
  -> Client 关闭连接
  -> Server 清理资源并退出
```

实现时要特别注意：

- stdout 只能输出 MCP 协议消息。
- 普通日志写 stderr。
- 启动失败时错误信息要能帮助定位配置问题。

## 练习 3：设计 Tools

先设计两个只读工具：

| Tool | 输入 | 输出 | 说明 |
| --- | --- | --- | --- |
| `search_notes` | `query`、`limit` | 匹配到的笔记列表 | 搜索本地学习笔记 |
| `get_note` | `note_id` | 笔记正文 | 读取指定笔记 |

`search_notes` 输入 schema 示例：

```json
{
  "name": "search_notes",
  "description": "搜索本地学习笔记。只搜索配置允许的数据目录，不读取任意本地路径。",
  "inputSchema": {
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
    "required": ["query"],
    "additionalProperties": false
  }
}
```

`get_note` 输入 schema 示例：

```json
{
  "name": "get_note",
  "description": "根据 note_id 读取学习笔记正文。不会读取任意文件路径。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "note_id": {
        "type": "string",
        "minLength": 1,
        "description": "笔记 ID，例如 mcp-basic"
      }
    },
    "required": ["note_id"],
    "additionalProperties": false
  }
}
```

练习要求：

- `query` 为空时返回清晰错误。
- 搜索不到结果时返回空列表，而不是程序崩溃。
- `note_id` 不存在时返回未找到错误。
- 工具不读取配置允许范围之外的文件。
- 默认只读，不提供删除、修改、上传能力。

## 练习 4：设计 Resources

Resources 用来暴露可读取上下文。推荐先定义 3 个资源 URI：

```text
notes://prompt/basic
notes://agent/basic
notes://mcp/basic
```

每个资源返回：

```json
{
  "contents": [
    {
      "uri": "notes://mcp/basic",
      "mimeType": "text/markdown",
      "text": "# MCP 基础\n..."
    }
  ]
}
```

练习要求：

- URI 命名清晰且稳定。
- Resource 只读。
- 找不到资源时返回明确错误。
- 不允许客户端把 URI 当成本地路径拼接读取。

## 练习 5：设计 Prompts

Prompts 是给客户端复用的提示词模板。先设计一个学习复盘模板：

```text
请基于以下学习笔记，帮助 {{level}} 学习者完成复盘：

主题：{{topic}}
笔记内容：{{notes}}

请输出：
1. 一句话总结
2. 3 个关键概念
3. 2 个常见误区
4. 下一步练习建议
5. 自检清单
```

练习要求：

- Prompt 模板要有名称和描述。
- 参数要明确，例如 `topic`、`notes`、`level`。
- `topic` 和 `notes` 缺失时返回参数错误。
- 不要在 Prompt 中写真实密钥或内部敏感信息。

## 练习 6：设计 Config

使用 `config.example.json` 描述运行配置：

```json
{
  "serverName": "learning-notes-mcp",
  "dataDir": "./data",
  "enabledTools": ["search_notes", "get_note"],
  "enabledResources": ["notes://prompt/basic", "notes://agent/basic", "notes://mcp/basic"],
  "enabledPrompts": ["study_review"],
  "permissions": {
    "readOnly": true,
    "allowWrite": false
  },
  "logLevel": "info"
}
```

练习要求：

- 配置文件只提供示例值。
- 不要提交真实 API Key。
- 读写权限要明确。
- Server 启动时校验必要配置。
- 禁用的 Tool、Resource、Prompt 不应该暴露给 Client。

## 练习 7：错误处理

请实现或伪实现统一错误结构：

```json
{
  "error": {
    "type": "INVALID_PARAMS",
    "message": "query 不能为空",
    "hint": "请传入至少 1 个字符的搜索关键词"
  }
}
```

至少覆盖：

| 场景 | 错误类型 |
| --- | --- |
| 参数缺失或为空 | `INVALID_PARAMS` |
| 笔记不存在 | `NOT_FOUND` |
| 读取配置外目录 | `PERMISSION_DENIED` |
| 数据文件损坏 | `INTERNAL_ERROR` 或 `DATA_ERROR` |
| 未启用工具 | `PERMISSION_DENIED` |

## 练习 8：客户端配置

连接到 AI 客户端时，建议使用本地开发配置，并确认命令、参数和工作目录都写清楚。

Claude Desktop / Claude Code 的配置核心类似：

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/lessons/06-mcp/04-exercises-lab/starter",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

说明：

- `/ABSOLUTE/PATH/...` 必须替换为本机绝对路径。
- `env` 里不要写真实密钥。
- 如果使用 TypeScript，替换为 `node dist/server.js` 或项目实际启动命令。

## 运行方式

不同语言和 SDK 的命令会不同。初学阶段可以先提供伪运行方式，等实现后再替换为真实命令。

Python 示例：

```bash
cd lessons/06-mcp/04-exercises-lab/starter
python server.py --config config.example.json
```

TypeScript 示例：

```bash
cd lessons/06-mcp/04-exercises-lab/starter
npm install
npm run dev -- --config config.example.json
```

## 调试清单

- [ ] 直接运行启动命令，确认 Server 不会立刻崩溃。
- [ ] 检查 `config.example.json` 路径是否正确。
- [ ] 检查 `cwd` 是否为项目目录。
- [ ] 检查 stdout 是否只输出协议消息。
- [ ] 检查 stderr 或日志文件中是否有启动错误。
- [ ] 用空 query 测试参数错误。
- [ ] 用不存在 note_id 测试未找到错误。
- [ ] 禁用某个 Tool 后确认它不再出现在列表里。

## 参考答案说明

参考答案建议放在 `answers/` 目录下。参考答案应展示：

1. 一个可启动的最小 MCP Server。
2. 至少 2 个 tools。
3. 至少 1 个 resource。
4. 至少 1 个 prompt。
5. 一个 `config.example.json`。
6. 清晰的错误处理。
7. Claude Desktop / Claude Code 配置示例。

参考答案不应包含：

- 真实 API Key。
- 真实内部系统地址。
- 需要特殊权限才能运行的依赖。

## 自检清单

- [ ] 我能说清楚 MCP Client/Server 生命周期。
- [ ] 我能说清楚 Tool、Resource、Prompt 的区别。
- [ ] 每个 Tool 都有输入 schema。
- [ ] Resource 是只读上下文，不负责执行动作。
- [ ] Prompt 模板参数清晰。
- [ ] Config 中没有真实密钥。
- [ ] Server 的能力边界明确。
- [ ] 错误处理区分参数错误、未找到、权限不足、内部错误。
- [ ] 客户端配置使用绝对路径和占位环境变量。
- [ ] 我能解释 stdio 与 SSE 的差异。
