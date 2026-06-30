# 06 MCP 阶段复盘

本阶段的核心是理解 MCP 如何把“工具、资源、提示词模板”从某个 Agent 内部抽离出来，变成可被多个 AI 客户端复用的标准服务。MCP Server 不是简单脚本集合，而是一个有协议边界、生命周期边界、权限边界和配置边界的上下文服务。

## 本阶段你应该掌握什么

完成 06-mcp 后，你应该能够说明：

1. MCP Client 是能力使用方，MCP Server 是能力提供方。
2. 一个 MCP 会话通常经历启动、initialize、能力发现、调用、关闭。
3. MCP 消息采用 JSON-RPC 2.0 风格，请求、响应、错误都应该结构化。
4. stdio 适合本地开发，SSE 适合远端服务但需要更强安全控制。
5. Tools 是可执行动作，Resources 是只读上下文，Prompts 是可复用提示词模板。
6. 一个 MCP Server 至少要考虑注册能力、输入 schema、错误处理、调试和配置管理。
7. Config 应该控制 Server 名称、数据目录、启用能力和权限边界。
8. MCP 可以让 Agent 更标准地接入外部系统，而不是在 Agent 代码里硬编码所有工具。

## 推荐复盘问题

### 1. 你的 Server 提供什么，不提供什么？

一个好的 MCP Server 应该有清晰边界。例如课程知识库 Server 可以提供：

- 搜索课程 Markdown。
- 读取允许范围内的课程页面。
- 暴露固定课程 Resource。
- 返回学习复盘 Prompt。

但它不应该默认提供：

- 删除本地文件。
- 读取任意路径。
- 读取 `.env`、密钥文件或用户主目录其他文件。
- 自动上传敏感资料。
- 在没有确认的情况下执行写操作。

### 2. Client/Server 生命周期是否讲得清楚？

请用自己的话复述：

```text
Client 读取配置
  -> 启动或连接 Server
  -> 建立 stdio 或 SSE 传输
  -> initialize / initialized
  -> list tools/resources/prompts
  -> callTool/readResource/getPrompt
  -> 返回结果或错误
  -> 关闭连接并清理资源
```

如果你只能解释 Tool 调用，却解释不清初始化和能力发现，说明对 MCP 还停留在“函数调用”层面。

### 3. Tools、Resources、Prompts 是否混在一起？

请检查：

- 如果它会执行动作或查询系统，通常是 Tool。
- 如果它是稳定、只读、可引用内容，通常是 Resource。
- 如果它是可复用的任务模板，通常是 Prompt。

不要把所有能力都做成 Tool。这样会让权限边界变得模糊。

### 4. 输入 schema 是否足够明确？

每个 Tool 都应该说明：

- 需要哪些参数。
- 参数类型是什么。
- 哪些参数必填。
- 参数为空或不合法时如何返回错误。
- 是否允许额外字段。
- 枚举值、长度、数量范围是什么。

输入 schema 是客户端正确调用工具的基础。schema 越含糊，模型越容易传错参数。

### 5. Config 是否只是摆设？

配置文件应该真正影响 Server 行为，例如：

- 禁用的 Tool 不注册。
- 不存在的 `courseRoot` 或 `dataDir` 会启动失败或提示错误。
- `readOnly=true` 时不允许写操作。
- `allowedDirs` 控制能读取哪些目录。
- 日志级别可以控制输出内容。

如果修改配置对系统没有影响，说明配置设计还没有落地。

### 6. 错误处理是否可诊断？

至少要区分：

| 类型 | 场景 | 用户可见信息 |
| --- | --- | --- |
| `INVALID_PARAMS` | query 为空 | 参数不合法，并说明哪个参数 |
| `NOT_FOUND` | note_id 或 URI 不存在 | 资源不存在 |
| `PERMISSION_DENIED` | 路径逃逸、只读模式写入 | 权限不足或不允许访问 |
| `UPSTREAM_ERROR` | 外部服务不可用 | 依赖暂不可用 |
| `INTERNAL_ERROR` | 未预期异常 | 内部错误，请看安全日志 |

对外错误要清楚，但不要泄露本地敏感路径、Token、Cookie、完整隐私字段。

### 7. stdio 和 SSE 的边界是否清楚？

stdio：

- 本地进程。
- stdin/stdout 交换 JSON-RPC。
- 适合本地课程知识库、文件系统、本地开发。
- stdout 不能打印普通日志。

SSE：

- 通常是远端 HTTP 长连接。
- 适合托管服务和多客户端共享。
- 必须关注 HTTPS、认证、授权、限流、审计。
- 不要把内部服务裸露到公网。

## 常见错误

### 错误 1：把 MCP Server 写成普通命令行脚本

表现：脚本能跑，但没有 tools/resources/prompts 的清晰注册关系，也没有 initialize 和能力发现概念。

改法：

- 单独建立 `tools/`、`resources/`、`prompts/` 模块。
- 在 `server` 入口统一注册能力。
- 为每种能力写清楚名称、描述和参数。
- 在 README 中说明 Client/Server 生命周期。

### 错误 2：Tool 没有输入 schema

表现：客户端不知道如何传参，调用失败后也不知道哪里错。

改法：

- 每个 Tool 都定义 JSON Schema 或等价结构。
- 参数缺失时返回明确错误。
- 在 README 中给出示例输入输出。
- 使用 `additionalProperties: false` 收紧参数。

### 错误 3：Resource 可以读取任意文件

表现：客户端传入路径后，Server 直接读取本地文件。

风险：可能泄露敏感文件。

改法：

- 使用固定 URI 或受控映射。
- 只允许读取配置范围内的数据。
- 不把用户输入直接拼接成本地文件路径。
- 对路径做 normalize/resolve 并校验是否仍在允许目录内。

### 错误 4：Config 中写入真实密钥

表现：`config.json` 或 README 示例里出现真实 Token、Cookie、API Key。

改法：

- 只提交 `config.example.json`。
- 使用占位符，例如 `${COURSE_API_TOKEN}`。
- 真实密钥通过环境变量或本地未提交配置提供。
- 日志中也要脱敏。

### 错误 5：错误信息不清楚

表现：工具失败后只返回“failed”。

改法：

- 区分参数错误、未找到、权限不足、内部错误。
- 错误信息对初学者友好。
- 日志记录必要上下文，但不要记录敏感信息。

### 错误 6：stdout 被日志污染

表现：本地命令看起来有输出，但客户端连接失败或卡住。

原因：stdio 模式下 stdout 是协议通道，普通日志会破坏 JSON-RPC 消息。

改法：

- 普通日志写 stderr。
- 调试信息写日志文件。
- 保证 stdout 只写 MCP 协议消息。

### 错误 7：客户端配置依赖当前 shell 环境

表现：终端能运行，Claude Desktop / Claude Code 不能运行。

原因：客户端启动时 PATH、工作目录、环境变量可能与终端不同。

改法：

- 配置 `cwd`。
- 使用绝对路径。
- 明确声明 env。
- 不依赖交互式 shell 初始化脚本。

## 检查清单

### 概念检查

- [ ] 我能解释 MCP Client 和 MCP Server 的关系。
- [ ] 我能复述 MCP 会话生命周期。
- [ ] 我能解释 JSON-RPC 请求、响应、错误的基本结构。
- [ ] 我能区分 Tool、Resource、Prompt。
- [ ] 我能说明 stdio 和 SSE 的适用场景。
- [ ] 我能说明为什么 MCP 对 Agent 工程有帮助。
- [ ] 我能解释为什么 Server 需要权限边界。

### 工程检查

- [ ] Server 入口负责统一注册能力。
- [ ] `tools/`、`resources/`、`prompts/` 目录职责清晰。
- [ ] 每个 Tool 都有输入 schema。
- [ ] Resource 使用稳定 URI，不暴露任意本地路径。
- [ ] Prompt 模板参数清晰。
- [ ] Config 能控制启用能力和权限。
- [ ] 默认不包含写操作，或写操作需要明确权限和确认。
- [ ] 日志不泄露真实密钥。
- [ ] stdout 不输出普通日志。
- [ ] Claude Desktop / Claude Code 配置示例使用占位路径和占位环境变量。

### 验收检查

- [ ] Server 可以在本地启动。
- [ ] 客户端可以列出 tools。
- [ ] `search_lessons` 或 `search_notes` 能处理正常查询和空查询。
- [ ] `get_lesson_page` 或 `get_note` 能处理存在和不存在的 ID/路径。
- [ ] 路径逃逸或越权访问会被拒绝。
- [ ] 至少一个 Resource 可以被读取。
- [ ] 至少一个 Prompt 可以被使用。
- [ ] 配置禁用某个工具后，该工具不会被暴露。
- [ ] 日志不包含 Token、Cookie、API Key 或私人数据。

## 阶段交付物建议

完成本阶段后，建议保留以下交付物：

1. MCP Server 项目 README。
2. `config.example.json`，只包含占位值。
3. 至少 2 个 Tool 的 schema 和示例输入输出。
4. Resource URI 到课程页面的映射说明。
5. 至少 1 个 Prompt 模板。
6. Claude Desktop / Claude Code 配置示例。
7. 调试记录：启动、正常调用、参数错误、未找到、权限拒绝。
8. 安全说明：默认只读、路径 allowlist、日志脱敏、密钥管理。

## 下一步

学完 MCP 后，可以把 05-agent 和 06-mcp 连接起来：

1. 让研究助手不再直接调用本地函数，而是通过 MCP Server 使用工具。
2. 把学习笔记作为 MCP Resources 提供给 Agent。
3. 把阶段复盘模板作为 MCP Prompt 提供给 Agent。
4. 在 Agent 工具日志中记录每次 MCP 调用。

继续学习时，可以关注：

- Claude Code 如何配置 MCP Server。
- Claude Desktop 如何加载本地 stdio Server。
- MCP Server 如何接入真实数据源。
- 写操作工具如何设计用户确认。
- 远端 SSE Server 如何做认证、授权、限流和审计。
- 多个 MCP Server 如何组合成 Agent 的工具生态。

当你能把一个 Agent 的工具能力抽象为 MCP Server，并能解释生命周期、schema、错误处理、调试和安全边界，就完成了从“单体 Agent 脚本”到“可复用 AI 工程能力”的关键一步。
