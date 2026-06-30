# MCP 练习参考答案

对应题目：[lessons/06-mcp/03-exercises.md](../../lessons/06-mcp/03-exercises.md)

这些答案用于做完练习后的复盘。请重点关注“为什么这样答”和“常见错误”。

## 练习 1：区分概念

### 参考答案

- MCP Client：发起连接和调用的一方，通常是 Claude Code、IDE 或 Agent 应用。
- MCP Server：暴露能力的一方，负责提供工具、资源和提示模板。
- Tool：可执行动作，例如搜索、查询、写入、调用 API。
- Resource：可读取上下文或资料，例如文件、文档、数据库 schema。
- Prompt：可复用提示模板，用于标准化某类任务说明。

### 为什么这样答

MCP 的核心是把外部上下文和能力标准化。Client 不直接知道每个系统细节，而是通过 Server 暴露的能力交互。

### 常见错误

- 把 MCP Server 当成模型本身。
- 把 Resource 设计成会修改状态的动作。
- 把 Prompt 和 Tool 混淆。
## 练习 2：判断适合做成什么

### 参考答案

| 能力 | 类型 | 原因 |
| --- | --- | --- |
| 读取项目 README | Resource | 稳定可读上下文。 |
| 查询某个用户资料 | Tool | 需要带参数查询外部系统。 |
| 代码审查提示词模板 | Prompt | 是复用任务说明。 |
| 修改工单状态 | Tool | 会执行写操作。 |
| 获取数据库表结构 | Resource 或 Tool | 静态 schema 可做 Resource；动态查询可做 Tool。 |
| 生成 PR 描述模板 | Prompt | 是标准化输出模板。 |

### 为什么这样答

分类的关键是：是否执行动作、是否只是读取上下文、是否是提示模板。写操作几乎都应做成 Tool，并加权限控制。

### 常见错误

- 把所有能力都做成 Tool。
- 让 Resource 执行修改操作。
- Prompt 中硬编码敏感信息。
## 练习 3：设计一个 Tool

### 参考答案

```json
{
  "name": "search_docs",
  "description": "在课程文档中按关键词搜索相关片段。",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "搜索关键词或问题"},
      "top_k": {"type": "integer", "default": 5, "minimum": 1, "maximum": 10}
    },
    "required": ["query"]
  },
  "risk_level": "low"
}
```

返回示例：

```json
{
  "results": [
    {"title": "Prompt 基础", "uri": "docs://ai-agent/prompt-basic", "snippet": "Prompt 是..."}
  ]
}
```

### 为什么这样答

搜索文档是只读能力，风险较低，但仍要限制 `top_k`，避免一次返回过多内容或造成资源浪费。

### 常见错误

- 不限制返回数量。
- 返回整篇文档，导致上下文膨胀。
- 不提供 uri，后续无法读取来源。
## 练习 4：设计一个 Resource

### 参考答案

```json
{
  "uri": "docs://ai-agent/prompt-basic",
  "name": "Prompt 基础",
  "description": "AI Agent 课程中关于 Prompt 基础概念和结构的入门文档。",
  "mimeType": "text/markdown",
  "source": "data/docs/prompt-basic.md"
}
```

### 为什么这样答

Resource 应是可读取、可引用、稳定定位的上下文。URI 使用语义化命名，`mimeType` 告诉客户端如何解析内容。

### 常见错误

- URI 不稳定或依赖本机绝对路径。
- 没有 mimeType，客户端不知道内容类型。
- Resource 读取时顺便执行写操作。
## 练习 5：权限分析

### 参考答案

| Tool | 是否需要确认 | 原因 |
| --- | --- | --- |
| read_file | 视范围而定 | 读项目普通文件可放行；读敏感路径需确认或禁止。 |
| delete_file | 需要 | 破坏性删除。 |
| query_database | 视数据而定 | 可能涉及隐私或业务数据。 |
| update_database | 需要 | 修改共享状态。 |
| send_message | 需要 | 对外发送内容。 |
| create_pull_request | 需要 | 影响协作系统并对他人可见。 |

### 为什么这样答

确认机制不是只看工具名，而是看数据敏感性、是否写入、是否对外可见、是否容易回滚。

### 常见错误

- 查询数据库默认低风险。
- 对发送消息不做预览确认。
- 删除类工具没有二次确认和日志。
## 练习 6：配置理解

### 参考答案

阅读 MCP 配置时应定位：

1. Server 名称：通常是配置对象的 key，例如 `filesystem`、`github`、`docs`。
2. 启动命令：`command` 和 `args` 字段共同决定如何启动。
3. 环境变量：`env` 字段或命令依赖的变量，例如 token、路径、模式。
4. 暴露能力：由 Server 类型推断，例如文件系统 Server 可能暴露读写文件，GitHub Server 可能暴露 issue/PR 操作。

### 为什么这样答

MCP 配置决定了 Agent 能接触哪些系统。读配置时要同时看启动方式和权限边界，不能只看名称。

### 常见错误

- 忽略 env 中的敏感 token。
- 不检查 args 中是否限制目录范围。
- 只看 Server 名称就判断能力。
## 练习 7：安全边界

### 参考答案

至少应采用这些策略：

1. 最小权限：Server 只访问完成任务所需的目录、API 和数据。
2. 读写分离：读取工具和修改工具分开设计，写操作必须确认。
3. 敏感信息过滤：不把 token、cookie、密码、私密数据返回给模型。
4. 审计日志：记录谁在何时调用了什么工具、参数和结果摘要。
5. 用户确认：删除、发送、修改、发布等动作执行前展示预览并确认。
6. 速率限制：防止循环调用或批量读取内部数据。
7. 环境变量管理：密钥只放本地环境或 secret 管理系统，不写入仓库。

### 为什么这样答

MCP Server 是 Agent 通往内部系统的桥。安全设计要假设模型可能误调用工具，也要假设外部内容可能诱导模型越权。

### 常见错误

- 只靠 Prompt 要求模型“不要泄露”。
- Server 暴露过宽目录或全库权限。
- 没有日志，事故后无法追踪。
