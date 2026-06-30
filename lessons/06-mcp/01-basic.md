# MCP 基础

## MCP 是什么

MCP 是 Model Context Protocol，可以理解为 AI 应用连接工具和数据源的一套标准协议。

它解决的问题是：不同 AI 客户端都需要访问文件、数据库、GitHub、内部系统，如果每个客户端都单独开发一套插件，会非常混乱。MCP 提供了一种统一方式。

## 基本角色

### MCP Client

MCP Client 是使用 MCP Server 能力的一方。

例如：

- Claude Code
- Claude Desktop
- IDE 插件
- 自己开发的 Agent 应用

### MCP Server

MCP Server 是提供工具、资源或提示词的一方。

例如：

- 文件系统 Server
- GitHub Server
- 数据库 Server
- 浏览器 Server
- 内部业务系统 Server

## MCP 能提供什么

### Tools

Tools 是可执行动作。

例如：

- 查询数据库
- 读取文件
- 搜索 GitHub Issue
- 创建工单
- 调用内部 API

Tools 通常会改变或查询外部世界，所以需要关注权限。

### Resources

Resources 是可读取资源。

例如：

- 某个文件内容
- 某张数据库表结构
- 某个接口文档
- 某个项目配置

Resources 更偏“上下文读取”。

### Prompts

Prompts 是可复用的提示词模板。

例如：

- 代码审查模板
- PR 总结模板
- 安全检查模板
- 故障排查模板

### Sampling

Sampling 是 MCP Server 请求模型生成内容的能力。

它让 Server 在某些场景下也可以借助模型能力，但实际使用时要非常注意权限和边界。

## JSON-RPC

MCP 底层通信通常基于 JSON-RPC 风格。

你可以先简单理解为：

```text
客户端发送结构化请求，服务端返回结构化响应。
```

## MCP 解决什么问题

- 工具接入标准化
- 数据源暴露标准化
- 工具可以被多个 AI 客户端复用
- 企业内部能力可以封装为 MCP Server
- Agent 不需要知道每个系统的私有接入细节

## 权限边界

MCP Server 连接真实系统，因此必须注意：

- 哪些工具可读？
- 哪些工具可写？
- 哪些操作需要用户确认？
- 是否会泄露敏感数据？
- 工具返回内容是否可信？

## 一句话总结

MCP 是让 AI Agent 标准化使用外部工具和上下文的协议。
