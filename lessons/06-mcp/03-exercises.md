# MCP 练习

这些练习覆盖 MCP 的端到端理解：从概念、协议、schema、配置，到调试、安全和课程知识库 Server 设计。

## 练习 1：区分概念

请解释下面概念的区别：

- MCP Client
- MCP Server
- Tool
- Resource
- Prompt
- Sampling

要求：每个概念至少写 2 句话，并举 1 个课程项目中的例子。

## 练习 2：画出生命周期

请画出或写出一个 stdio MCP Server 的生命周期：

1. Client 如何启动 Server？
2. initialize 阶段交换什么信息？
3. Client 如何发现 tools/resources/prompts？
4. 调用 Tool 时 JSON-RPC 请求和响应大致是什么样？
5. 会话结束时如何关闭？

加分：说明如果 Server 在 stdout 打印普通日志，会发生什么问题。

## 练习 3：判断适合做成什么

判断下面能力适合做成 Tool、Resource 还是 Prompt，并说明原因：

1. 读取项目 README
2. 查询某个用户资料
3. 代码审查提示词模板
4. 修改工单状态
5. 获取数据库表结构
6. 生成 PR 描述模板
7. 暴露 `lessons/06-mcp/01-basic.md` 的只读内容
8. 根据学习笔记生成复盘提纲
9. 搜索课程知识库中的 Markdown 文件

## 练习 4：设计一个 Tool

设计一个 `search_docs` MCP Tool。

要求包含：

- name
- description
- inputSchema
- 返回结果示例
- 参数错误示例
- 风险等级
- 权限策略

必须包含的 schema 约束：

- `query` 是必填字符串，不能为空。
- `limit` 是可选整数，范围 1 到 10。
- `section` 是可选枚举：`prompt`、`agent`、`mcp`。
- 不允许额外字段。

## 练习 5：设计一个 Resource

设计一个文档资源：

```text
docs://ai-agent/prompt-basic
```

说明它的名称、描述、mimeType、内容来源和访问边界。

继续设计 2 个课程知识库资源：

```text
course://06-mcp/basic
course://06-mcp/review
```

要求说明：

- URI 为什么稳定？
- 是否允许客户端传入任意本地路径？
- 找不到资源时应该返回什么错误？

## 练习 6：设计一个 Prompt

设计一个 `study_review` MCP Prompt。

要求：

- 参数包含 `topic`、`notes`、`level`。
- `topic` 和 `notes` 必填。
- 输出格式包含：一句话总结、关键概念、常见误区、练习建议、自检清单。
- Prompt 中不得包含真实密钥、内部地址、私人数据。

## 练习 7：权限分析

下面 MCP Tool 哪些需要用户确认？哪些应该默认禁用？

- read_file
- delete_file
- query_database
- update_database
- send_message
- create_pull_request
- search_course_notes
- export_private_notes

说明原因，并为每个 Tool 标注风险等级：低、中、高。

## 练习 8：JSON-RPC 理解

阅读下面请求，回答问题：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "get_note",
    "arguments": {
      "note_id": "mcp-basic"
    }
  }
}
```

问题：

1. 这是请求、响应还是通知？
2. 请求 ID 是什么？有什么作用？
3. 调用的 Tool 名称是什么？
4. 参数是什么？
5. 如果 `note_id` 不存在，应该如何返回结构化错误？

## 练习 9：配置理解

阅读一个 MCP 配置，回答：

```json
{
  "mcpServers": {
    "learning-notes": {
      "command": "python",
      "args": ["-m", "src.server", "--config", "config.example.json"],
      "cwd": "/ABSOLUTE/PATH/learning_notes_mcp",
      "env": {
        "LOG_LEVEL": "info",
        "COURSE_DATA_DIR": "/ABSOLUTE/PATH/lessons"
      }
    }
  }
}
```

问题：

1. Server 名称是什么？
2. 启动命令是什么？
3. 工作目录是什么？为什么建议使用绝对路径？
4. 需要哪些环境变量？
5. 这个 Server 可能暴露哪些能力？
6. 配置里是否包含真实密钥？如果需要密钥应该如何处理？

## 练习 10：stdio 与 SSE 对比

请对比 stdio 和 SSE：

| 维度 | stdio | SSE |
| --- | --- | --- |
| 连接方式 |  |  |
| 适合场景 |  |  |
| 安全重点 |  |  |
| 调试重点 |  |  |
| 常见错误 |  |  |

要求至少写出 3 个 stdio 调试注意点和 3 个 SSE 安全注意点。

## 练习 11：错误处理设计

为课程知识库 MCP Server 设计错误处理表：

| 场景 | 错误类型 | 用户可见信息 | 日志是否记录细节 |
| --- | --- | --- | --- |
| query 为空 |  |  |  |
| note_id 不存在 |  |  |  |
| 读取了未授权目录 |  |  |  |
| JSON 数据文件损坏 |  |  |  |
| 未预期异常 |  |  |  |

要求：用户可见信息要清楚，但不能泄露本地敏感路径或密钥。

## 练习 12：调试排障

下面是几个现象，请写出可能原因和排查步骤：

1. Claude Desktop 中看不到 `learning-notes` Server。
2. Server 本地命令能启动，但客户端连接后一直卡住。
3. Tool 列出来了，但模型总是传错参数。
4. `search_notes` 本地测试正常，客户端调用时报找不到数据目录。
5. 日志中出现了 Token 或 Cookie。

每个现象至少写 3 个排查步骤。

## 练习 13：课程知识库 MCP Server 设计

设计一个“课程知识库 MCP Server”，用于暴露本仓库中的课程资料。

最低能力：

- Tool：`search_lessons(query, lesson_id?, limit?)`
- Tool：`get_lesson_page(path)`
- Resource：`course://06-mcp/basic`
- Resource：`course://06-mcp/review`
- Prompt：`lesson_review(topic, notes, level?)`

约束：

- 只能读取配置允许的课程目录。
- 不允许读取 `.env`、`.git`、密钥文件、用户主目录其他文件。
- 默认只读。
- Tool 参数必须有 schema。
- 错误要区分参数错误、未找到、权限不足、内部错误。

输出：写出你的目录结构、配置示例、Tool schema、Resource URI 映射和安全策略。

## 练习 14：安全边界

如果 MCP Server 连接了内部系统，应该如何避免敏感信息泄露？

至少写出 8 条策略，并覆盖：

- 配置管理
- 日志脱敏
- 最小权限
- 写操作确认
- 输出过滤
- 远端传输安全
- 审计
- Prompt injection 防护
