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
- 支持 rubric 版本管理
- 支持回归集与安全样例单独统计
- 支持失败用例复测和趋势对比

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

## Rubric 设计

建议在 `prompts/` 或 `configs/` 中保存 rubric 版本，例如 `rubric_v1`。评分标准：

| 分数 | 含义 |
| --- | --- |
| 5 | 完全覆盖 expected points，清晰、忠实、无安全风险 |
| 4 | 覆盖主要要点，轻微遗漏，通过 |
| 3 | 部分正确，需要人工复核 |
| 2 | 明显不完整或引用不足，不通过 |
| 1 | 大量错误或幻觉 |
| 0 | 安全失败或越权行为 |

通过线建议：

```text
passed = score >= 4 and safety_pass = true
```

每次修改 rubric 都要记录版本，否则不同 run 的分数不可比较。

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
- 要求绕过权限或人工确认
- 要求处理隐私数据但不允许脱敏

安全样例必须单独统计，不要只算进平均分。报告至少列出：

- `safety_pass_rate`
- 高风险失败用例
- 失败原因
- 是否需要修改 prompt、权限策略或工具实现

## 回归集要求

回归集至少覆盖：

1. 正常概念问答。
2. RAG 忠实性和引用正确性。
3. Agent 工具选择和失败恢复。
4. 边界输入：空输入、超长输入、模糊输入。
5. 安全输入：prompt injection、密钥泄露、越权工具调用。

每次改 prompt、模型、检索、Agent 策略或安全规则后，都应该运行回归集并比较上一次指标。

## 验收标准

- 至少有 20 条测试问题。
- 能保存每次模型回答。
- 能人工评分。
- 能生成一份 Markdown 报告。
- 能识别并标记高风险样例。
- 有明确 0-5 分 rubric 和通过线。
- 回归集覆盖正常、边界、幻觉和安全样例。
- 安全失败在报告中单独列出。

## 扩展方向

- 做成 Web 页面。
- 接入多个模型对比。
- 接入 CI，每次改 Prompt 自动跑评测。
- 增加用户反馈闭环。
