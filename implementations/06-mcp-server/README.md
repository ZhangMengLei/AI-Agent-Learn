# 06 Mini MCP Server

这是一个用 Python 标准库实现的 MCP / JSON-RPC 概念教学 Demo。它不是生产级 MCP Server，也不依赖真实 MCP SDK，目标是帮助初学者理解 tools、resources、prompts 的边界。

## 你会看到什么

- `initialize`：返回 server 信息和能力。
- `tools/list`、`tools/call`：列出并调用工具。
- `resources/list`、`resources/read`：列出并读取资源。
- `prompts/list`、`prompts/get`：列出并渲染提示模板。
- JSON-RPC 成功响应和错误响应。

## 运行方式

```bash
python implementations/06-mcp-server/main.py --demo
python implementations/06-mcp-server/main.py --request-json '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

也可以使用 Makefile：

```bash
make demo-mcp
```

## 学习重点

- Tool 是可执行动作，Resource 是可读取上下文，Prompt 是可复用提示模板。
- MCP Server 应返回结构化结果和清晰错误。
- 高风险工具应加权限控制；本 Demo 只提供只读教学能力。

## 数据来源

- `data/notes/ai-agent-notes.json`
- `data/docs/mcp-basic.md`
- `data/docs/prompt-basic.md`

## 运行测试

```bash
python -m unittest tests/test_mcp_server.py
```
