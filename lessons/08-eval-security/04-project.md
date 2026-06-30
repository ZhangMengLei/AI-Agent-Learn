# Eval / Security 实战项目：AI 应用评测面板

## 项目目标

做一个简单的 AI 应用评测面板，用来记录模型回答、人工评分、成本、延迟和安全风险。

## 功能要求

### 基础功能

- 维护一组测试问题
- 批量运行模型回答
- 记录每次回答
- 人工给回答打分
- 统计平均分、失败率和幻觉率

### 进阶功能

- 记录 token 和成本
- 记录响应延迟
- 标记高风险输入
- 使用 LLM-as-Judge 初步评分
- 对比不同模型或不同 Prompt 的效果

## 推荐目录

```text
eval-dashboard/
  README.md
  datasets/
    golden.jsonl
  runs/
    run-001.jsonl
  reports/
  prompts/
    judge.md
  src/
    run_eval.py
    score.py
    report.py
```

## 数据集格式

```json
{
  "id": "case-001",
  "category": "prompt",
  "question": "Prompt 是什么？",
  "expected_points": [
    "Prompt 是给 AI 的任务说明",
    "清晰 Prompt 能提升输出稳定性"
  ],
  "risk_level": "low"
}
```

## 运行结果格式

```json
{
  "case_id": "case-001",
  "model": "model-name",
  "answer": "...",
  "input_tokens": 500,
  "output_tokens": 120,
  "latency_ms": 1000,
  "score": 4,
  "hallucination": false,
  "error": null
}
```

## 报告指标

至少统计：

- 测试用例数量
- 平均分
- 正确率
- 幻觉率
- 平均延迟
- 总 token 消耗
- 失败用例列表

## 安全检查

评测集中应该包含一些安全样例：

- 要求泄露系统提示词
- 要求输出 API Key
- 工具结果中包含恶意指令
- 用户要求执行高风险动作

## 验收标准

- 至少有 20 条测试问题。
- 能保存每次模型回答。
- 能人工评分。
- 能生成一份 Markdown 报告。
- 能识别并标记高风险样例。

## 扩展方向

- 做成 Web 页面。
- 接入多个模型对比。
- 接入 CI，每次改 Prompt 自动跑评测。
- 增加用户反馈闭环。
