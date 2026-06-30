# MCP 练习工程说明

本目录用于完成 06-mcp 阶段的工程化练习。目标是理解一个自定义 MCP Server 应该如何设计，而不是一开始就接入复杂外部系统。请先用本地数据实现最小 Server，再逐步补充 tools、resources、prompts 和 config。

## 练习目标

完成后你应该能够：

1. 说明 MCP Client 与 MCP Server 的关系。
2. 区分 Tools、Resources、Prompts 的职责。
3. 设计一个最小 MCP Server 的目录结构。
4. 为工具定义输入 schema 和清晰错误返回。
5. 使用配置文件描述 Server 名称、数据目录、启用的工具和权限边界。

## 推荐目录

建议在本目录下按下面结构组织练习代码：

```text
03-exercises-lab/
  README.md
  starter/
    server.py 或 server.ts       # MCP Server 入口
    config.example.json          # 示例配置，不写真实密钥
    tools/
      search_notes.py 或 searchNotes.ts
    resources/
      notes.py 或 notes.ts
    prompts/
      review.py 或 review.ts
    data/
      notes.json
  answers/
    README.md                    # 参考答案说明
```

说明：

- `tools/` 放可执行动作。
- `resources/` 放可读取上下文。
- `prompts/` 放可复用提示词模板。
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

## 练习 2：设计 Tools

先设计两个只读工具：

| Tool | 输入 | 输出 | 说明 |
| --- | --- | --- | --- |
| `search_notes` | `query` | 匹配到的笔记列表 | 搜索本地学习笔记 |
| `get_note` | `note_id` | 笔记正文 | 读取指定笔记 |

工具输入必须有 schema。示例：

```json
{
  "name": "search_notes",
  "description": "搜索本地学习笔记",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "搜索关键词"
      }
    },
    "required": ["query"]
  }
}
```

练习要求：

- `query` 为空时返回清晰错误。
- 搜索不到结果时返回空列表，而不是程序崩溃。
- 工具不读取配置允许范围之外的文件。

## 练习 3：设计 Resources

Resources 用来暴露可读取上下文。推荐先定义 3 个资源 URI：

```text
notes://prompt/basic
notes://agent/basic
notes://mcp/basic
```

每个资源返回：

```json
{
  "uri": "notes://mcp/basic",
  "mimeType": "text/markdown",
  "text": "# MCP 基础\n..."
}
```

练习要求：

- URI 命名清晰。
- Resource 只读。
- 找不到资源时返回明确错误。

## 练习 4：设计 Prompts

Prompts 是给客户端复用的提示词模板。先设计一个学习复盘模板：

```text
请基于以下学习笔记，帮助初学者完成复盘：

主题：{{topic}}
笔记内容：{{notes}}

请输出：
1. 一句话总结
2. 3 个关键概念
3. 2 个常见误区
4. 下一步练习建议
```

练习要求：

- Prompt 模板要有名称和描述。
- 参数要明确，例如 `topic`、`notes`。
- 不要在 Prompt 中写真实密钥或内部敏感信息。

## 练习 5：设计 Config

使用 `config.example.json` 描述运行配置：

```json
{
  "serverName": "learning-notes-mcp",
  "dataDir": "./data",
  "enabledTools": ["search_notes", "get_note"],
  "permissions": {
    "readOnly": true,
    "allowWrite": false
  }
}
```

练习要求：

- 配置文件只提供示例值。
- 不要提交真实 API Key。
- 读写权限要明确。
- Server 启动时校验必要配置。

## 运行方式

不同语言和 SDK 的命令会不同。初学阶段可以先提供伪运行方式，等实现后再替换为真实命令。

Python 示例：

```bash
cd lessons/06-mcp/03-exercises-lab/starter
python server.py --config config.example.json
```

TypeScript 示例：

```bash
cd lessons/06-mcp/03-exercises-lab/starter
npm install
npm run dev -- --config config.example.json
```

连接到 AI 客户端时，建议使用本地开发配置，并确认命令、参数和工作目录都写清楚。

## 参考答案说明

参考答案建议放在 `answers/` 目录下。参考答案应展示：

1. 一个可启动的最小 MCP Server。
2. 至少 2 个 tools。
3. 至少 1 个 resource。
4. 至少 1 个 prompt。
5. 一个 `config.example.json`。
6. 清晰的错误处理。

参考答案不应包含：

- 真实 API Key。
- 真实内部系统地址。
- 需要特殊权限才能运行的依赖。

## 自检清单

- [ ] 我能说清楚 Tool、Resource、Prompt 的区别。
- [ ] 每个 Tool 都有输入 schema。
- [ ] Resource 是只读上下文，不负责执行动作。
- [ ] Prompt 模板参数清晰。
- [ ] Config 中没有真实密钥。
- [ ] Server 的能力边界明确。
