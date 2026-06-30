# 06 MCP

## 学习目标

理解 MCP（Model Context Protocol）如何让 AI 应用标准化连接外部工具和数据源。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习工程](04-exercises-lab/README.md)
- [实战项目](05-project.md)
- [项目工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)
- [MCP Server Lab：课程知识库最小实现指南](mcp-server-lab/README.md)

## 核心概念

- MCP Client
- MCP Server
- Tools
- Resources
- Prompts
- Sampling
- JSON-RPC
- stdio / SSE
- Schema
- 错误处理
- 调试
- 权限与边界

## 学习任务

1. 理解 MCP Client 和 MCP Server 的关系与生命周期。
2. 区分 Tools、Resources、Prompts。
3. 理解 JSON-RPC、stdio 和 SSE 的基本概念。
4. 阅读 Claude Desktop / Claude Code 的 MCP Server 配置。
5. 设计一个有 schema、错误处理和权限边界的自定义 MCP Tool。
6. 实现一个课程知识库 MCP Server。

## 实战项目

做一个课程知识库 MCP Server。
