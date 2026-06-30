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

## 可运行参考实现

- [Mini MCP Server Demo](../../implementations/06-mcp-server/)：用标准库模拟 MCP / JSON-RPC server、tools、resources 和 prompts。
- 运行命令：`make demo-mcp`

## 核心概念

- MCP Client
- MCP Server
- Tools
- Resources
- Prompts
- Sampling
- JSON-RPC
- 权限与边界

## 学习任务

1. 理解 MCP Client 和 MCP Server 的关系。
2. 区分 Tools、Resources、Prompts。
3. 阅读一个 MCP Server 配置。
4. 设计一个自定义 MCP Tool。
5. 实现一个最小 MCP Server。

## 实战项目

做一个自定义 MCP Server。
