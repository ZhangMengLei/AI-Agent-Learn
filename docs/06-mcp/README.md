# 06 MCP

## 学习目标

理解 MCP（Model Context Protocol）如何让 AI 应用标准化连接外部工具和数据源。

## 核心概念

- MCP Client
- MCP Server
- Tools
- Resources
- Prompts
- Sampling
- JSON-RPC
- 权限与边界

## MCP 解决什么问题

- 统一工具接入方式
- 统一数据源暴露方式
- 避免每个 AI 应用重复开发插件
- 让不同客户端复用同一个 Server

## 常见 MCP Server

- Filesystem
- GitHub
- Database
- Browser
- Slack
- Jira
- 自定义业务系统

## 学习任务

1. 安装并配置一个现成 MCP Server。
2. 理解 MCP Server 如何声明 tool。
3. 自己写一个最小 MCP Server。
4. 给 MCP tool 增加输入 schema。
5. 在 AI 客户端中调用 MCP tool。

## 实战项目

做一个 `自定义 MCP Server`：

- 提供 2-3 个工具
- 返回结构化结果
- 支持错误处理
- 对敏感操作做权限控制

## 检查标准

- 是否理解 Client 和 Server 的关系？
- 是否能区分 Tools、Resources、Prompts？
- 是否能设计清晰的输入输出 schema？
