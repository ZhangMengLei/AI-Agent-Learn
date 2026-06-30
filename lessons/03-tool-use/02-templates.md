# Tool Use 常用模板

## 工具定义模板

```json
{
  "name": "get_weather",
  "description": "根据城市名称查询当前天气。适合回答天气、温度、降雨相关问题。",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称，例如北京、上海"
      }
    },
    "required": ["city"]
  }
}
```

## 工具调用记录模板

```json
{
  "tool_name": "get_weather",
  "arguments": {
    "city": "北京"
  },
  "status": "success",
  "result": {
    "temperature": "26°C",
    "condition": "晴"
  },
  "error": null
}
```

## 工具执行流程模板

```text
1. 接收用户问题
2. 把可用工具列表交给模型
3. 模型决定是否调用工具
4. 如果需要工具，解析工具名称和参数
5. 校验参数
6. 判断是否需要人工确认
7. 执行工具
8. 将工具结果交回模型
9. 模型生成最终回答
```

## 权限确认模板

```text
工具名称：delete_file
风险等级：高
即将执行：删除文件 /tmp/test.txt
是否继续？[y/N]
```

## 错误处理模板

```json
{
  "tool_name": "query_database",
  "status": "error",
  "result": null,
  "error": {
    "type": "validation_error",
    "message": "缺少必填参数 table_name"
  }
}
```

## 工具结果回传模板

```text
工具 get_weather 返回：
城市：北京
天气：晴
温度：26°C

请基于工具结果回答用户，不要编造工具结果中没有的信息。
```

## 工具设计检查清单

- 工具是否只做一件事？
- 参数是否足够少？
- 描述是否能帮助模型正确选择？
- 返回格式是否稳定？
- 错误信息是否清晰？
- 是否区分低风险和高风险工具？
