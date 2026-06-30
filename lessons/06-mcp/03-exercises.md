# MCP 练习

## 练习 1：区分概念

请解释下面概念的区别：

- MCP Client
- MCP Server
- Tool
- Resource
- Prompt

## 练习 2：判断适合做成什么

判断下面能力适合做成 Tool、Resource 还是 Prompt：

1. 读取项目 README
2. 查询某个用户资料
3. 代码审查提示词模板
4. 修改工单状态
5. 获取数据库表结构
6. 生成 PR 描述模板

## 练习 3：设计一个 Tool

设计一个 `search_docs` MCP Tool。

要求包含：

- name
- description
- input_schema
- 返回结果示例
- 风险等级

## 练习 4：设计一个 Resource

设计一个文档资源：

```text
docs://ai-agent/prompt-basic
```

说明它的名称、描述、mimeType 和内容来源。

## 练习 5：权限分析

下面 MCP Tool 哪些需要用户确认？

- read_file
- delete_file
- query_database
- update_database
- send_message
- create_pull_request

说明原因。

## 练习 6：配置理解

阅读一个 MCP 配置，回答：

1. Server 名称是什么？
2. 启动命令是什么？
3. 需要哪些环境变量？
4. 这个 Server 可能暴露哪些能力？

## 练习 7：安全边界

如果 MCP Server 连接了内部系统，应该如何避免敏感信息泄露？

至少写出 5 条策略。
