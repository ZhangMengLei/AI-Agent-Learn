# MCP 实战项目：课程知识库 MCP Server

## 项目目标

做一个最小但完整的 MCP Server，让 AI 客户端可以通过标准协议访问本课程知识库。这个项目的重点不是接入复杂外部系统，而是把 MCP 的端到端链路跑通：生命周期、JSON-RPC、stdio 配置、tools/resources/prompts 设计、schema、错误处理、调试、权限与安全。

完成后，你应该能把本仓库的课程资料封装为一个本地只读 MCP Server，并接入 Claude Desktop 或 Claude Code。

## 项目场景

构建一个 `course-knowledge-mcp`：

- 面向：学习本课程的 AI 客户端和 Agent。
- 数据源：本仓库 `lessons/` 下的 Markdown 课程资料。
- 默认权限：只读。
- 传输方式：优先 stdio。
- 扩展方向：未来可托管为远端 SSE Server，但必须增加认证、授权、HTTPS、审计和限流。

## 推荐功能

### Tools

```text
search_lessons(query, lesson_id?, limit?)  搜索课程 Markdown 文档
get_lesson_page(path)                      读取允许范围内的课程页面
list_lessons()                             列出课程章节
```

最低要求至少实现前两个 Tool。

### Resources

```text
course://01-prompt/basic
course://05-agent/review
course://06-mcp/basic
course://06-mcp/review
```

Resource 用于暴露稳定、常用、只读的课程页面，不接收任意本地路径。

### Prompts

```text
lesson_review(topic, notes, level?)        基于课程笔记生成学习复盘
project_checklist(project_name, goals)     生成项目验收清单
```

最低要求至少实现 `lesson_review`。

## 推荐目录

Python 版本：

```text
course-knowledge-mcp/
  README.md
  pyproject.toml
  config.example.json
  src/
    server.py
    config.py
    types.py
    tools/
      __init__.py
      search_lessons.py
      get_lesson_page.py
      list_lessons.py
    resources/
      __init__.py
      course_resources.py
    prompts/
      __init__.py
      lesson_review.py
    utils/
      errors.py
      logger.py
      paths.py
  tests/
    test_tools.py
    test_resources.py
  data/
    resource_map.example.json
```

TypeScript 版本：

```text
course-knowledge-mcp/
  README.md
  package.json
  tsconfig.json
  config.example.json
  src/
    server.ts
    config.ts
    types.ts
    tools/
      index.ts
      searchLessons.ts
      getLessonPage.ts
      listLessons.ts
    resources/
      index.ts
      courseResources.ts
    prompts/
      index.ts
      lessonReview.ts
    utils/
      errors.ts
      logger.ts
      paths.ts
  tests/
    tools.test.ts
    resources.test.ts
  data/
    resource_map.example.json
```

## Client/Server 生命周期要求

项目 README 中必须说明你的 Server 如何经历以下流程：

```text
1. Client 读取 mcpServers 配置。
2. Client 使用 command/args/cwd 启动本地 Server。
3. Client 与 Server 通过 stdio 交换 JSON-RPC 消息。
4. Client 发送 initialize。
5. Server 返回 serverInfo 和 capabilities。
6. Client 发送 initialized。
7. Client 发现 tools/resources/prompts。
8. Client 根据模型需要调用 Tool、读取 Resource 或获取 Prompt。
9. Server 校验 schema、权限和路径边界。
10. Server 返回结构化结果或结构化错误。
11. Client 关闭连接，Server 释放资源。
```

实现注意：普通日志不能写 stdout，避免破坏 stdio JSON-RPC 通道。

## Tool 设计

### Tool 1：search_lessons

作用：搜索课程 Markdown 文档。

输入 schema：

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "minLength": 1,
      "description": "搜索关键词，不能为空"
    },
    "lesson_id": {
      "type": "string",
      "description": "可选课程 ID，例如 06-mcp"
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
```

输出建议：

```json
{
  "matches": [
    {
      "path": "lessons/06-mcp/01-basic.md",
      "title": "MCP 基础",
      "preview": "MCP 是 Model Context Protocol...",
      "score": 0.87
    }
  ]
}
```

边界：

- 只搜索配置允许的课程根目录。
- 默认排除 `.git`、`.env`、`node_modules`、隐藏目录、密钥文件。
- 搜索不到返回空数组，不崩溃。

### Tool 2：get_lesson_page

作用：读取课程页面 Markdown。

输入 schema：

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

输出建议：

```json
{
  "path": "lessons/06-mcp/01-basic.md",
  "mimeType": "text/markdown",
  "content": "# MCP 基础\n..."
}
```

边界：

- 只允许读取课程根目录内的 Markdown 文件。
- 不能使用 `../` 逃逸目录。
- 不允许读取 `.env`、密钥文件、二进制文件或用户主目录任意文件。

### Tool 3：list_lessons

作用：列出课程章节。

输入 schema：

```json
{
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

输出建议：

```json
{
  "lessons": [
    {
      "lesson_id": "06-mcp",
      "title": "MCP",
      "pages": ["01-basic.md", "02-templates.md"]
    }
  ]
}
```

## Resources 设计

Resource URI 与本地文件使用显式映射，不允许客户端自由拼接路径。

```json
{
  "course://06-mcp/basic": "lessons/06-mcp/01-basic.md",
  "course://06-mcp/templates": "lessons/06-mcp/02-templates.md",
  "course://06-mcp/review": "lessons/06-mcp/07-review.md"
}
```

Resource 返回：

```json
{
  "contents": [
    {
      "uri": "course://06-mcp/basic",
      "mimeType": "text/markdown",
      "text": "# MCP 基础\n..."
    }
  ]
}
```

要求：

- URI 稳定。
- 找不到 URI 时返回 `NOT_FOUND`。
- 映射目标仍要经过路径安全校验。

## Prompts 设计

### Prompt：lesson_review

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `topic` | 是 | 学习主题 |
| `notes` | 是 | 课程笔记或 Resource 内容 |
| `level` | 否 | 学习者水平，默认 beginner |

模板：

```text
你是一名 AI 大模型课程助教。请基于以下课程笔记为 {{level}} 学习者生成复盘。

主题：{{topic}}
笔记：{{notes}}

请输出：
1. 一句话总结
2. 5 个关键概念
3. 3 个常见误区
4. 3 个动手练习建议
5. 自检清单
```

要求：

- 参数缺失时返回 `INVALID_PARAMS`。
- Prompt 不包含真实密钥、内部地址或私人数据。
- 输出结构稳定，便于教学检查。

## Config 设计

`config.example.json` 建议包含：

```json
{
  "serverName": "course-knowledge-mcp",
  "courseRoot": "/ABSOLUTE/PATH/AI-Agent-Learn",
  "allowedDirs": ["lessons"],
  "enabledTools": ["search_lessons", "get_lesson_page", "list_lessons"],
  "enabledResources": ["course://06-mcp/basic", "course://06-mcp/templates", "course://06-mcp/review"],
  "enabledPrompts": ["lesson_review"],
  "permissions": {
    "readOnly": true,
    "allowWrite": false
  },
  "logLevel": "info"
}
```

原则：

- 示例配置可以提交，真实密钥不可以提交。
- `courseRoot` 在示例中用占位绝对路径。
- 默认只读。
- 启动时校验 `courseRoot`、`allowedDirs` 和权限配置。
- 禁用的能力不应该出现在客户端列表里。

## 客户端配置示例

### Claude Desktop

```json
{
  "mcpServers": {
    "course-knowledge": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/course-knowledge-mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

### Claude Code

```json
{
  "mcpServers": {
    "course-knowledge": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/course-knowledge-mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

配置检查：

- 使用绝对路径。
- `command` 在客户端环境中可执行。
- `cwd` 指向 MCP Server 项目目录。
- 示例不包含真实 API Key。
- 如果未来接入远端服务，密钥从环境变量读取。

## 调试要求

至少验证以下情况：

1. Server 能直接用启动命令运行。
2. 客户端能发现 tools/resources/prompts。
3. `search_lessons({"query":"MCP"})` 返回结果。
4. `search_lessons({"query":""})` 返回参数错误。
5. `get_lesson_page({"path":"lessons/06-mcp/01-basic.md"})` 返回 Markdown。
6. `get_lesson_page({"path":"../.env"})` 返回权限错误。
7. 读取 `course://06-mcp/basic` 返回 Markdown。
8. 读取不存在 URI 返回未找到错误。
9. `lesson_review` 参数缺失时返回参数错误。
10. 日志不打印真实密钥，stdout 不出现普通日志。

## 权限与安全要求

最低安全基线：

- 默认只读，不实现写操作。
- 只读取 `allowedDirs` 中允许的课程目录。
- 所有路径做 normalize/resolve 后再判断是否仍在允许目录内。
- 拒绝 `../` 逃逸、绝对路径输入、隐藏目录、密钥文件和二进制文件。
- 不提交真实 API Key、Token、Cookie。
- 日志脱敏，不记录完整敏感参数。
- Tool 返回内容视为不可信上下文，不把课程内容当系统指令执行。
- 未来接入 SSE 时必须使用 HTTPS、认证、授权、限流和审计。

## 验收标准

- MCP Server 可以启动。
- 至少提供 2 个 tools。
- 至少提供 1 个 resource。
- 至少提供 1 个 prompt。
- 工具输入有 schema。
- 错误信息清晰。
- 不暴露真实密钥。
- Claude Desktop / Claude Code 配置示例完整。
- README 说明生命周期、stdio/SSE 概念、调试方式和安全边界。

## 扩展方向

- 接入 GitHub，但只读查询 issue/PR，写操作默认禁用。
- 接入数据库，但只允许白名单查询。
- 为课程搜索增加标签和章节过滤。
- 为写操作增加用户确认和审计日志。
- 将 MCP Server 接入前面章节实现的 Agent，让 Agent 不再直接读取课程文件。
