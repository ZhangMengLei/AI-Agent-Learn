# MCP Server Lab：课程知识库最小实现指南

本目录用于补充 06 MCP 的端到端教学内容，目标是指导你实现一个“课程知识库 MCP Server”的最小版本。这里不放真实密钥，不调用网络，不要求连接真实内部系统。

## 目标能力

最小 Server 应该提供：

- Tools
  - `search_lessons`：搜索课程 Markdown。
  - `get_lesson_page`：读取允许范围内的课程页面。
- Resources
  - `course://06-mcp/basic`
  - `course://06-mcp/review`
- Prompts
  - `lesson_review`
- Config
  - 控制课程根目录、启用能力、只读权限、日志级别。

## 推荐目录

```text
mcp-server-lab/
  README.md
  course_knowledge_mcp/
    config.example.json
    src/
      server.py
      config.py
      tools/
        search_lessons.py
        get_lesson_page.py
      resources/
        course_resources.py
      prompts/
        lesson_review.py
      utils/
        errors.py
        logger.py
        paths.py
    data/
      resource_map.example.json
```

如果你选择 TypeScript，可以把 `.py` 替换为 `.ts`，结构保持一致。

## Server 生命周期

请在实现中对应下面步骤：

```text
1. 解析 --config 参数。
2. 读取 config.example.json。
3. 校验 courseRoot 和 allowedDirs。
4. 创建 MCP Server，声明 name/version/capabilities。
5. 注册启用的 tools/resources/prompts。
6. 使用 stdio 传输启动。
7. 等待 Client 发送 initialize。
8. 响应 tools/list、resources/list、prompts/list。
9. 处理 tools/call、resources/read、prompts/get。
10. 连接关闭后释放资源。
```

## JSON-RPC 调用示例

教学时可以用下面请求理解 Tool 调用结构：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_lessons",
    "arguments": {
      "query": "MCP",
      "lesson_id": "06-mcp",
      "limit": 5
    }
  }
}
```

成功结果可以返回：

```json
{
  "matches": [
    {
      "path": "lessons/06-mcp/01-basic.md",
      "title": "MCP 基础",
      "preview": "MCP 是 Model Context Protocol..."
    }
  ]
}
```

参数错误可以返回：

```json
{
  "error": {
    "type": "INVALID_PARAMS",
    "message": "query 不能为空"
  }
}
```

## Tool schema

### search_lessons

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1,
      "description": "搜索关键词"
    },
    "lesson_id": {
      "type": "string",
      "description": "可选课程 ID，例如 06-mcp"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "description": "最多返回条数"
    }
  },
  "required": ["query"],
  "additionalProperties": false
}
```

### get_lesson_page

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "minLength": 1,
      "description": "课程页面相对路径，例如 lessons/06-mcp/01-basic.md"
    }
  },
  "required": ["path"],
  "additionalProperties": false
}
```

## Resource 映射

使用固定 URI 映射课程文件：

```json
{
  "course://06-mcp/basic": "lessons/06-mcp/01-basic.md",
  "course://06-mcp/review": "lessons/06-mcp/07-review.md"
}
```

要求：

- URI 不等于本地路径。
- 读取 URI 时仍要做路径安全校验。
- 不存在的 URI 返回 `NOT_FOUND`。

## Prompt 模板

`lesson_review`：

```text
你是一名 AI 大模型课程助教。请基于以下课程笔记为 {{level}} 学习者生成复盘。

主题：{{topic}}
笔记：{{notes}}

请输出：
1. 一句话总结
2. 关键概念
3. 常见误区
4. 练习建议
5. 自检清单
```

参数：

- `topic`：必填。
- `notes`：必填。
- `level`：可选，默认 `beginner`。

## config.example.json

```json
{
  "serverName": "course-knowledge-mcp",
  "courseRoot": "/ABSOLUTE/PATH/AI-Agent-Learn",
  "allowedDirs": ["lessons"],
  "enabledTools": ["search_lessons", "get_lesson_page"],
  "enabledResources": ["course://06-mcp/basic", "course://06-mcp/review"],
  "enabledPrompts": ["lesson_review"],
  "permissions": {
    "readOnly": true,
    "allowWrite": false
  },
  "logLevel": "info"
}
```

## Claude Desktop / Claude Code 配置示例

```json
{
  "mcpServers": {
    "course-knowledge": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/lessons/06-mcp/mcp-server-lab/course_knowledge_mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

说明：

- 使用本机绝对路径替换 `/ABSOLUTE/PATH/...`。
- 不要在配置中写真实 Token、Cookie、API Key。
- 如果未来需要密钥，使用环境变量，并确保本地私有配置不提交。

## stdio 与 SSE

本实验默认 stdio：

- Client 启动本地进程。
- 通过 stdin/stdout 交换 JSON-RPC。
- stdout 只能输出协议消息。
- 日志写 stderr。

SSE 作为扩展方向：

- 适合远端 Server。
- 必须使用 HTTPS。
- 必须有认证、授权、限流和审计。
- 不要把内部服务直接暴露到公网。

## 安全要求

- 默认只读。
- 不实现删除、修改、上传能力。
- 只允许读取 `allowedDirs`。
- 拒绝绝对路径、`../`、隐藏目录、密钥文件、非 Markdown 文件。
- 日志脱敏，不记录 Token、Cookie、API Key。
- Tool 返回内容作为不可信上下文，不作为系统指令执行。

## 调试与验收

至少完成以下检查：

- [ ] Server 启动命令可运行。
- [ ] Client 能发现 `search_lessons` 和 `get_lesson_page`。
- [ ] `search_lessons({"query":"MCP"})` 返回结果。
- [ ] `search_lessons({"query":""})` 返回 `INVALID_PARAMS`。
- [ ] `get_lesson_page({"path":"lessons/06-mcp/01-basic.md"})` 返回 Markdown。
- [ ] `get_lesson_page({"path":"../.env"})` 返回 `PERMISSION_DENIED`。
- [ ] `course://06-mcp/basic` 可读取。
- [ ] 不存在 Resource 返回 `NOT_FOUND`。
- [ ] `lesson_review` 缺少 `topic` 或 `notes` 时返回参数错误。
- [ ] stdout 没有普通日志。
