# MCP 实战项目：自定义 MCP Server

## 项目目标

做一个最小 MCP Server，让 AI 客户端可以通过标准协议调用你的工具和资源。

## 推荐功能

先做一个学习型 MCP Server，提供：

- 查询学习笔记
- 搜索本地 Markdown 文档
- 返回 Prompt 模板

## 推荐工具

```text
search_notes(query)       搜索学习笔记
get_note(title)           读取指定笔记
list_prompt_templates()   列出 Prompt 模板
```

## 推荐资源

```text
notes://prompt/basic
notes://agent/basic
notes://mcp/basic
```

## 推荐目录

```text
my-learning-mcp/
  README.md
  src/
    server.ts 或 server.py
    tools/
      search_notes.ts
      get_note.ts
    resources/
      notes.ts
    prompts/
      review.ts
  notes/
  config.example.json
```

## 开发步骤

1. 创建 MCP Server 项目。
2. 定义一个最小 tool。
3. 在本地启动 Server。
4. 在 AI 客户端中配置 Server。
5. 测试工具是否能被调用。
6. 增加 Resource。
7. 增加 Prompt 模板。
8. 增加错误处理和日志。

## 验收标准

- MCP Server 可以启动。
- 至少提供 2 个 tools。
- 至少提供 1 个 resource。
- 工具输入有 schema。
- 错误信息清晰。
- 不暴露真实密钥。

## 扩展方向

- 接入 GitHub。
- 接入数据库。
- 接入公司内部 API。
- 为写操作增加用户确认。
- 将 MCP Server 接入 Claude Code。
