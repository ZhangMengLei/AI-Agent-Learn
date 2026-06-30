# MCP 常用模板

## MCP Server 项目结构模板

```text
my-mcp-server/
  README.md
  package.json 或 pyproject.toml
  src/
    server.ts 或 server.py
    tools/
    resources/
    prompts/
  config.example.json
```

## Tool 定义模板

```json
{
  "name": "query_user_profile",
  "description": "根据用户 ID 查询用户基础资料，只返回非敏感字段。",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "用户 ID"
      }
    },
    "required": ["user_id"]
  }
}
```

## Tool 返回模板

```json
{
  "content": [
    {
      "type": "text",
      "text": "用户昵称：Alice\n用户等级：VIP"
    }
  ]
}
```

## Resource 定义模板

```json
{
  "uri": "docs://agent/intro",
  "name": "Agent 入门文档",
  "description": "介绍 Agent 基础概念的文档",
  "mimeType": "text/markdown"
}
```

## Prompt 定义模板

```json
{
  "name": "review_code",
  "description": "对代码变更进行审查",
  "arguments": [
    {
      "name": "diff",
      "description": "代码 diff 内容",
      "required": true
    }
  ]
}
```

## 客户端配置示例

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/my-mcp-server/dist/server.js"],
      "env": {
        "API_TOKEN": "使用环境变量，不要写死真实 token"
      }
    }
  }
}
```

## 权限设计模板

```text
工具名称：update_ticket
风险等级：中
能力：修改工单状态
权限策略：执行前展示修改内容，并要求用户确认
日志：记录操作者、时间、参数、结果
```

## MCP Server 检查清单

- Tool 名称是否清晰？
- 输入 schema 是否准确？
- 返回格式是否稳定？
- 是否过滤敏感字段？
- 写操作是否需要确认？
- 错误信息是否可理解？
