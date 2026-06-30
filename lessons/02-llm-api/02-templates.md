# LLM API 常用模板

## 基础调用伪代码

```text
1. 读取用户输入
2. 构造 messages
3. 调用模型 API
4. 获取 assistant 回复
5. 输出给用户
```

## Messages 模板

```json
[
  {
    "role": "system",
    "content": "你是一个简洁、准确的 AI 助手。"
  },
  {
    "role": "user",
    "content": "请解释什么是 Agent。"
  }
]
```

## 多轮对话模板

```json
[
  {
    "role": "system",
    "content": "你是一个 AI 学习助手。"
  },
  {
    "role": "user",
    "content": "什么是 Prompt？"
  },
  {
    "role": "assistant",
    "content": "Prompt 是给 AI 的任务说明书。"
  },
  {
    "role": "user",
    "content": "那 System Prompt 是什么？"
  }
]
```

## 调用日志模板

每次调用建议记录：

```json
{
  "timestamp": "2026-06-30T10:00:00Z",
  "model": "model-name",
  "input_tokens": 0,
  "output_tokens": 0,
  "latency_ms": 0,
  "success": true,
  "error": null
}
```

## 错误处理模板

```text
如果 API 调用失败：
1. 判断是否是参数错误
2. 判断是否是 API Key 或权限问题
3. 判断是否是频率限制
4. 判断是否是网络问题
5. 给用户返回可理解的错误信息
```

## 流式输出流程

```text
1. 发起 streaming 请求
2. 接收模型增量输出
3. 每收到一段就打印一段
4. 直到结束事件
5. 保存完整回答
```
