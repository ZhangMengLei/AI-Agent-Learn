# MCP 项目实现工程说明：自定义学习笔记 MCP Server

本项目实验用于把 06-mcp 阶段的概念落到一个工程设计中：实现一个自定义学习笔记 MCP Server。它向 AI 客户端提供本地学习资料搜索、资源读取和复盘提示词模板。

本项目重点是 Server 的工程边界：`tools / resources / prompts / config`。请优先保证结构清楚、能力可解释、权限边界明确，再考虑接入更多外部系统。

## 项目目标

实现一个最小 MCP Server，支持：

1. 通过 Tool 搜索学习笔记。
2. 通过 Tool 读取指定笔记。
3. 通过 Resource 暴露固定学习资料。
4. 通过 Prompt 提供学习复盘模板。
5. 通过 Config 控制数据目录、启用工具和只读权限。

建议所有数据先放在本地 `data/` 目录中，不接入真实数据库或内部 API。

## 推荐文件结构

TypeScript 版本：

```text
04-project-lab/
  README.md
  learning-notes-mcp/
    package.json
    tsconfig.json
    config.example.json
    src/
      server.ts
      config.ts
      types.ts
      tools/
        index.ts
        searchNotes.ts
        getNote.ts
      resources/
        index.ts
        noteResources.ts
      prompts/
        index.ts
        reviewPrompt.ts
      data/
        notes.json
      utils/
        errors.ts
        logger.ts
```

Python 版本：

```text
04-project-lab/
  README.md
  learning_notes_mcp/
    pyproject.toml
    config.example.json
    src/
      server.py
      config.py
      types.py
      tools/
        __init__.py
        search_notes.py
        get_note.py
      resources/
        __init__.py
        note_resources.py
      prompts/
        __init__.py
        review_prompt.py
      data/
        notes.json
      utils/
        errors.py
        logger.py
```

## 模块职责

| 模块 | 主要职责 |
| --- | --- |
| `server` | 创建 MCP Server，注册 tools/resources/prompts |
| `config` | 读取和校验配置 |
| `types` | 定义 Note、ToolResult、Config 等结构 |
| `tools` | 提供可执行工具，例如搜索和读取笔记 |
| `resources` | 提供只读资源，例如固定笔记 URI |
| `prompts` | 提供复用提示词模板 |
| `utils/errors` | 统一错误信息 |
| `utils/logger` | 输出启动和调用日志，避免打印敏感信息 |

## Config 设计

`config.example.json` 建议包含：

```json
{
  "serverName": "learning-notes-mcp",
  "dataDir": "./src/data",
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

设计原则：

- 示例配置可以提交，真实密钥不可以提交。
- 默认只读。
- 工具、资源、提示词是否启用由配置控制。
- 启动时校验 `dataDir` 是否存在、权限配置是否合理。

## Tools 设计

### Tool 1：search_notes

作用：根据关键词搜索本地学习笔记。

输入 schema：

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "搜索关键词"
    },
    "limit": {
      "type": "number",
      "description": "最多返回条数"
    }
  },
  "required": ["query"]
}
```

输出建议：

```json
{
  "matches": [
    {
      "note_id": "mcp-basic",
      "title": "MCP 基础",
      "preview": "MCP 是连接 AI 应用与外部工具的标准协议..."
    }
  ]
}
```

### Tool 2：get_note

作用：读取指定笔记全文。

输入 schema：

```json
{
  "type": "object",
  "properties": {
    "note_id": {
      "type": "string",
      "description": "笔记 ID"
    }
  },
  "required": ["note_id"]
}
```

输出建议：

```json
{
  "note_id": "mcp-basic",
  "title": "MCP 基础",
  "content": "# MCP 基础\n..."
}
```

错误处理要求：

- 参数缺失：返回“缺少必填参数”。
- 笔记不存在：返回“未找到指定笔记”。
- 配置禁用工具：返回“工具未启用”。

## Resources 设计

Resources 适合暴露稳定、只读、可引用的上下文。

推荐 URI：

```text
notes://prompt/basic
notes://agent/basic
notes://mcp/basic
```

资源返回建议：

```json
{
  "uri": "notes://agent/basic",
  "mimeType": "text/markdown",
  "text": "# Agent 基础\nAgent 是围绕目标持续执行的系统..."
}
```

设计原则：

- Resource 不执行写操作。
- URI 要稳定。
- 找不到资源时返回明确错误。
- 不把本地任意文件路径直接暴露给客户端。

## Prompts 设计

### Prompt：study_review

作用：根据学习笔记生成阶段复盘。

参数：

| 参数 | 说明 |
| --- | --- |
| `topic` | 学习主题 |
| `notes` | 笔记内容 |
| `level` | 学习者水平，例如 beginner |

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

## 实现步骤

### 第 1 步：准备数据

创建 `notes.json`，包含少量学习笔记：

```json
[
  {
    "note_id": "mcp-basic",
    "title": "MCP 基础",
    "tags": ["mcp", "protocol"],
    "content": "MCP 是 Model Context Protocol..."
  }
]
```

### 第 2 步：读取配置

实现配置加载：

- 默认读取 `config.example.json`。
- 支持通过命令行参数传入配置路径。
- 校验 `serverName`、`dataDir`、`permissions`。

### 第 3 步：注册 Tools

在 Server 启动时根据 `enabledTools` 注册工具。不要把未启用工具暴露给客户端。

### 第 4 步：注册 Resources

将固定 URI 映射到本地笔记内容。注意不要允许客户端通过 URI 读取任意本地文件。

### 第 5 步：注册 Prompts

注册 `study_review`，并检查必填参数是否存在。

### 第 6 步：本地联调

联调时重点观察：

- Server 是否能启动。
- 客户端能否列出 tools。
- `search_notes` 参数为空时是否返回错误。
- `get_note` 查询不存在 ID 时是否返回错误。
- Resource URI 不存在时是否返回错误。
- Prompt 参数缺失时是否返回错误。

## 运行方式

TypeScript 示例：

```bash
cd lessons/06-mcp/04-project-lab/learning-notes-mcp
npm install
npm run dev -- --config config.example.json
```

Python 示例：

```bash
cd lessons/06-mcp/04-project-lab/learning_notes_mcp
python -m src.server --config config.example.json
```

客户端配置示例应使用占位命令，不写真实密钥：

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"]
    }
  }
}
```

## 验收方式

### 基础验收

- [ ] Server 可以启动。
- [ ] 至少注册 2 个 tools：`search_notes`、`get_note`。
- [ ] 每个 tool 都有输入 schema。
- [ ] 至少注册 1 个 resource。
- [ ] 至少注册 1 个 prompt。
- [ ] `config.example.json` 中没有真实密钥。
- [ ] 默认权限是只读。

### 功能验收

- [ ] `search_notes({"query":"MCP"})` 能返回匹配笔记。
- [ ] `get_note({"note_id":"mcp-basic"})` 能返回正文。
- [ ] 读取 `notes://mcp/basic` 能返回 Markdown 文本。
- [ ] 调用 `study_review` 能生成带参数的提示词。

### 异常验收

- [ ] `search_notes({"query":""})` 返回参数错误。
- [ ] `get_note({"note_id":"not-exist"})` 返回未找到。
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
