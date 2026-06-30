# Eval / Security 常用模板

## 测试集模板

```json
{
  "id": "case-001",
  "category": "rag",
  "question": "Agent 和 Chatbot 有什么区别？",
  "expected_points": [
    "Chatbot 主要回答问题",
    "Agent 会围绕目标规划和执行",
    "Agent 可以调用工具"
  ],
  "risk_level": "low"
}
```

## 评分表模板

```json
{
  "case_id": "case-001",
  "answer": "...",
  "score": 4,
  "max_score": 5,
  "correct": true,
  "hallucination": false,
  "missing_points": ["没有提到工具调用"],
  "comment": "整体正确，但不够完整"
}
```

## 调用日志模板

```json
{
  "request_id": "req-001",
  "timestamp": "2026-06-30T10:00:00Z",
  "model": "model-name",
  "input_tokens": 1000,
  "output_tokens": 300,
  "latency_ms": 1500,
  "cost": 0.01,
  "success": true,
  "error": null
}
```

## 安全风险清单

```text
输入风险：
- Prompt Injection
- Jailbreak
- 恶意文件内容

工具风险：
- 越权读取
- 越权写入
- 命令注入
- SQL 注入

数据风险：
- API Key 泄露
- 用户隐私泄露
- 日志保存敏感数据
```

## LLM-as-Judge Prompt 模板

```text
你是 AI 回答质量评审员。

请根据标准答案要点评估模型回答。

评分标准：
1. 5 分：完全正确，覆盖所有要点
2. 4 分：基本正确，缺少少量细节
3. 3 分：部分正确，有明显遗漏
4. 2 分：大部分错误
5. 1 分：完全错误或答非所问

问题：
{{question}}

标准要点：
{{expected_points}}

模型回答：
{{answer}}

请输出 JSON：
{
  "score": 0,
  "correct": false,
  "hallucination": false,
  "missing_points": [],
  "comment": ""
}
```

## 权限控制模板

```text
低风险：自动执行，记录日志
中风险：执行前提示用户确认
高风险：默认拒绝，除非用户明确授权
```
