# MCP 项目实现工程说明：课程知识库 MCP Server

本项目实验用于把 06-mcp 阶段的概念落到一个端到端工程中：实现一个自定义课程知识库 MCP Server。它向 AI 客户端提供本仓库课程资料搜索、资源读取和复盘提示词模板。

本项目重点是 Server 的工程边界：生命周期、JSON-RPC、stdio 传输、`tools / resources / prompts / config`、schema、错误处理、调试、权限与安全。请优先保证结构清楚、能力可解释、权限边界明确，再考虑接入更多外部系统。

## 项目目标

实现一个最小 MCP Server，支持：

1. 通过 Tool 搜索课程 Markdown 文档。
2. 通过 Tool 读取指定课程页面。
3. 通过 Resource 暴露固定课程资料。
4. 通过 Prompt 提供学习复盘模板。
5. 通过 Config 控制课程根目录、启用能力和只读权限。
6. 提供 Claude Desktop / Claude Code 本地配置示例。
7. 提供可重复的本地调试和验收步骤。

建议所有数据先来自本仓库 `lessons/` 目录，不接入真实数据库、内部 API 或需要网络的服务。

## 端到端调用链

请在实现和 README 中体现下面链路：

```text
Claude Desktop / Claude Code
  -> 读取 mcpServers 配置
  -> 按 command/args/cwd 启动 course-knowledge-mcp
  -> 通过 stdio 建立 JSON-RPC 通道
  -> initialize / initialized
  -> tools/list、resources/list、prompts/list
  -> tools/call: search_lessons 或 get_lesson_page
  -> resources/read: course://06-mcp/basic
  -> prompts/get: lesson_review
  -> Server 返回结构化结果或结构化错误
```

关键要求：

- stdout 只输出 MCP 协议消息。
- 普通日志写 stderr 或日志文件。
- 所有 Tool 参数先 schema 校验，再执行业务逻辑。
- 所有路径先 normalize/resolve，再做 allowlist 校验。

## 推荐文件结构

Python 版本：

```text
06-project-lab/
  README.md
  course_knowledge_mcp/
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
      data/
        resource_map.example.json
      utils/
        errors.py
        logger.py
        paths.py
    tests/
      test_tools.py
      test_resources.py
      test_paths.py
```

TypeScript 版本：

```text
06-project-lab/
  README.md
  course-knowledge-mcp/
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
      data/
        resource_map.example.json
      utils/
        errors.ts
        logger.ts
        paths.ts
    tests/
      tools.test.ts
      resources.test.ts
      paths.test.ts
```

## 模块职责

| 模块 | 主要职责 |
| --- | --- |
| `server` | 创建 MCP Server，声明 serverInfo/capabilities，注册 tools/resources/prompts，选择 stdio 传输 |
| `config` | 读取和校验配置，控制课程目录、启用能力、只读权限 |
| `types` | 定义 LessonPage、ToolResult、Config、ResourceMapping 等结构 |
| `tools` | 提供可执行工具，例如搜索和读取课程页面 |
| `resources` | 提供只读资源，例如固定课程 URI |
| `prompts` | 提供复用提示词模板 |
| `utils/errors` | 统一错误类型和错误转换 |
| `utils/logger` | 输出启动和调用日志，避免打印敏感信息，避免写 stdout |
| `utils/paths` | 路径 normalize/resolve、安全边界检查、文件类型过滤 |

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

设计原则：

- 示例配置可以提交，真实密钥不可以提交。
- 默认只读。
- 工具、资源、提示词是否启用由配置控制。
- 启动时校验 `courseRoot` 是否存在、`allowedDirs` 是否在根目录内、权限配置是否合理。
- `allowWrite=false` 时不注册任何写操作。
- 如果以后需要密钥，只从环境变量读取，并在示例中使用 `${ENV_NAME}` 占位。

## Tools 设计

### Tool 1：search_lessons

作用：根据关键词搜索本仓库课程 Markdown。

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
      "preview": "MCP 是 Model Context Protocol，可以理解为...",
      "score": 0.87
    }
  ]
}
```

错误处理要求：

- `query` 为空：返回 `INVALID_PARAMS`。
- `lesson_id` 不存在：返回空结果或 `NOT_FOUND`，二选一并在 README 中说明。
- 数据目录不存在：返回 `INTERNAL_ERROR`，日志记录安全细节。
- 搜索不到：返回空 `matches`，不崩溃。

### Tool 2：get_lesson_page

作用：读取指定课程页面全文。

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

错误处理要求：

- 参数缺失：返回 `INVALID_PARAMS`。
- 文件不存在：返回 `NOT_FOUND`。
- 路径逃逸、绝对路径、隐藏目录、密钥文件：返回 `PERMISSION_DENIED`。
- 非 Markdown 文件：返回 `PERMISSION_DENIED` 或 `INVALID_PARAMS`，并说明策略。

### Tool 3：list_lessons

作用：列出课程章节和页面，便于客户端发现课程结构。

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
      "pages": ["01-basic.md", "02-templates.md", "07-review.md"]
    }
  ]
}
```

## Resources 设计

Resources 适合暴露稳定、只读、可引用的上下文。

推荐 URI：

```text
course://01-prompt/basic
course://05-agent/review
course://06-mcp/basic
course://06-mcp/templates
course://06-mcp/review
```

资源映射示例：

```json
{
  "course://06-mcp/basic": "lessons/06-mcp/01-basic.md",
  "course://06-mcp/templates": "lessons/06-mcp/02-templates.md",
  "course://06-mcp/review": "lessons/06-mcp/07-review.md"
}
```

资源返回建议：

```json
{
  "contents": [
    {
      "uri": "course://06-mcp/basic",
      "mimeType": "text/markdown",
      "text": "# MCP 基础\nMCP 是 Model Context Protocol..."
    }
  ]
}
```

设计原则：

- Resource 不执行写操作。
- URI 要稳定，不跟随本地文件任意变动。
- 找不到资源时返回 `NOT_FOUND`。
- 不把本地任意文件路径直接暴露给客户端。
- Resource 映射目标也要经过路径安全校验。

## Prompts 设计

### Prompt：lesson_review

作用：根据课程笔记生成阶段复盘。

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `topic` | 是 | 学习主题 |
| `notes` | 是 | 课程笔记内容 |
| `level` | 否 | 学习者水平，例如 beginner |

模板示例：

```text
你是一名 AI 大模型课程助教。请基于以下笔记为 {{level}} 学习者生成复盘。

主题：{{topic}}
笔记：{{notes}}

请输出：
1. 一句话总结
2. 关键概念
3. 常见误区
4. 练习建议
5. 自检清单
```

设计原则：

- Prompt 只描述任务，不包含真实密钥。
- 参数名清晰。
- 输出格式稳定，便于教学检查。
- 将来自 Resource 或 Tool 的内容视为资料，不视为系统指令。

## JSON-RPC 与传输说明

### stdio

本项目默认使用 stdio：Client 启动本地 Server 进程，双方通过 stdin/stdout 交换 JSON-RPC 消息。

注意：

- stdout 只能输出 JSON-RPC 消息。
- stderr 可以输出调试日志。
- 本地命令和客户端配置的工作目录可能不同，建议配置 `cwd` 和绝对路径。

### SSE

SSE 可作为扩展方向。若未来将课程知识库 Server 托管为远端服务，需要增加：

- HTTPS。
- 认证与授权。
- 用户级权限隔离。
- 请求限流。
- 审计日志。
- 敏感内容过滤。

本实验不要求实现 SSE，也不要调用网络。

## 实现步骤

### 第 1 步：准备资源映射

创建 `resource_map.example.json`，包含少量课程资源映射：

```json
{
  "course://06-mcp/basic": "lessons/06-mcp/01-basic.md",
  "course://06-mcp/review": "lessons/06-mcp/07-review.md"
}
```

### 第 2 步：读取配置

实现配置加载：

- 默认读取 `config.example.json`。
- 支持通过命令行参数传入配置路径。
- 校验 `serverName`、`courseRoot`、`allowedDirs`、`permissions`。
- 禁止把真实密钥写入配置示例。

### 第 3 步：实现路径安全

路径安全是本项目重点之一：

1. 将用户输入路径与 `courseRoot` 组合。
2. 对路径做 normalize/resolve。
3. 判断解析后的路径是否仍在允许目录内。
4. 拒绝绝对路径、`../` 逃逸、隐藏目录、密钥文件、非 Markdown 文件。

### 第 4 步：注册 Tools

在 Server 启动时根据 `enabledTools` 注册工具。不要把未启用工具暴露给客户端。

### 第 5 步：注册 Resources

将固定 URI 映射到课程 Markdown。注意不要允许客户端通过 URI 读取任意本地文件。

### 第 6 步：注册 Prompts

注册 `lesson_review`，并检查必填参数是否存在。

### 第 7 步：本地联调

联调时重点观察：

- Server 是否能启动。
- 客户端能否列出 tools。
- `search_lessons` 参数为空时是否返回错误。
- `get_lesson_page` 查询不存在路径时是否返回错误。
- 路径逃逸是否被拒绝。
- Resource URI 不存在时是否返回错误。
- Prompt 参数缺失时是否返回错误。

## 运行方式

TypeScript 示例：

```bash
cd lessons/06-mcp/06-project-lab/course-knowledge-mcp
npm install
npm run dev -- --config config.example.json
```

Python 示例：

```bash
cd lessons/06-mcp/06-project-lab/course_knowledge_mcp
python -m src.server --config config.example.json
```

## 客户端配置示例

示例应使用占位命令和占位路径，不写真实密钥。

Claude Desktop / Claude Code 示例：

```json
{
  "mcpServers": {
    "course-knowledge": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/lessons/06-mcp/06-project-lab/course_knowledge_mcp",
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

## 验收方式

### 基础验收

- [ ] Server 可以启动。
- [ ] 至少注册 2 个 tools：`search_lessons`、`get_lesson_page`。
- [ ] 每个 tool 都有输入 schema。
- [ ] 至少注册 1 个 resource。
- [ ] 至少注册 1 个 prompt。
- [ ] `config.example.json` 中没有真实密钥。
- [ ] 默认权限是只读。
- [ ] stdout 不输出普通日志。

### 功能验收

- [ ] `search_lessons({"query":"MCP"})` 能返回匹配课程页面。
- [ ] `get_lesson_page({"path":"lessons/06-mcp/01-basic.md"})` 能返回正文。
- [ ] 读取 `course://06-mcp/basic` 能返回 Markdown 文本。
- [ ] 调用 `lesson_review` 能生成带参数的提示词。

### 异常验收

- [ ] `search_lessons({"query":""})` 返回参数错误。
- [ ] `get_lesson_page({"path":"not-exist.md"})` 返回未找到。
- [ ] `get_lesson_page({"path":"../.env"})` 返回权限错误。
- [ ] 未启用工具不会出现在工具列表中。
- [ ] 不存在的 Resource URI 返回明确错误。
- [ ] 日志不打印真实密钥、Token 或 Cookie。

## 进阶扩展

基础版本完成后，可以继续尝试：

- 增加写操作工具，但必须加入用户确认和权限开关。
- 为搜索结果增加标签过滤。
- 将资源映射到更多课程阶段。
- 为 Prompt 增加不同学习水平参数。
- 接入 Agent 阶段的研究助手，让研究助手通过 MCP 使用工具。
- 将 stdio Server 改造成远端 SSE Server，并补齐认证、授权、审计和限流。
