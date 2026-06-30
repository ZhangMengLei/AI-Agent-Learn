# 08 Eval / Security 项目实验工程

本项目实验要求你实现一个最小可用的 AI 应用评测工程。它围绕 golden dataset、批量运行、评分、日志和报告生成展开，帮助你从“感觉模型不错”升级为“用数据判断模型是否可用”。

## 项目目标

构建一个本地教学版评测工程，能够完成：

1. 维护一份 golden dataset。
2. 批量生成或导入模型回答。
3. 对回答进行人工评分或规则评分。
4. 记录 token、延迟、错误和安全标签。
5. 生成 Markdown 评测报告。
6. 标记安全风险并给出改进建议。

本项目可以使用模拟模型输出，不要求真实调用任何模型 API。不要写入真实 API Key。

## 推荐文件结构

请在 `04-project-lab/` 下实现以下结构：

```text
04-project-lab/
  README.md
  eval-lab/
    datasets/
      golden.jsonl
    prompts/
      app_prompt.md
      judge_prompt.md
    src/
      run_eval.py
      score.py
      report.py
      schema.py
    runs/
      run-001.jsonl
    logs/
      run-001.log.jsonl
    reports/
      run-001-report.md
    configs/
      eval.config.example.json
    checklists/
      dataset.md
      scoring.md
      security.md
```

目录说明：

- `datasets/golden.jsonl`：黄金测试集。
- `prompts/`：应用 prompt 和 judge prompt 示例。
- `src/run_eval.py`：批量读取用例并生成回答，可先用 mock answer。
- `src/score.py`：根据 expected points、人工分或 judge 结果打分。
- `src/report.py`：汇总运行结果并生成报告。
- `src/schema.py`：集中定义数据字段，避免格式混乱。
- `runs/`：每次评测的模型回答和评分结果。
- `logs/`：调用日志，必须脱敏。
- `reports/`：面向人阅读的 Markdown 报告。
- `configs/`：教学配置示例，不包含真实密钥。
- `checklists/`：数据集、评分和安全验收清单。

## 数据格式设计

### Golden dataset

`datasets/golden.jsonl` 每行一个用例：

```json
{"id":"case-001","category":"concept","question":"什么是 prompt caching？","expected_points":["复用稳定上下文","降低延迟和成本","适合长系统提示或长文档"],"risk_level":"low","tags":["cost","cache"]}
```

建议至少 20 条：

- 8 条基础概念。
- 4 条多步骤推理。
- 3 条 RAG/上下文忠实性。
- 2 条不知道就承认不知道。
- 3 条安全风险样例。

### Run result

`runs/run-001.jsonl` 每行一个结果：

```json
{"run_id":"run-001","case_id":"case-001","model":"mock-model","prompt_version":"app_prompt_v1","answer":"...","score":4,"passed":true,"safety_pass":true,"hallucination":false,"input_tokens":300,"output_tokens":80,"latency_ms":850,"error":null}
```

### Log

`logs/run-001.log.jsonl` 只记录排障需要的元数据：

```json
{"request_id":"req-001","run_id":"run-001","case_id":"case-001","model":"mock-model","success":true,"latency_ms":850,"input_tokens":300,"output_tokens":80,"error_type":null,"risk_tags":[],"created_at":"2026-06-30T10:00:00Z"}
```

不要记录真实 API Key、cookie、token、完整隐私输入、生产用户标识。

## 实现步骤

### 第 1 步：定义 schema

在 `src/schema.py` 中定义三个核心结构：

- `EvalCase`：测试用例。
- `RunResult`：模型回答和评分。
- `InvocationLog`：调用日志。

初学者可以先用 Python 字典，不必上复杂框架。关键是字段稳定。

### 第 2 步：准备 golden dataset

创建 `datasets/golden.jsonl`，保证覆盖：

- 正常问题。
- 边界问题。
- 容易幻觉的问题。
- prompt injection。
- 敏感信息泄露请求。
- 高风险工具操作请求。

每条用例都要有 expected points，否则后续评分会变成主观感受。

### 第 3 步：实现 run_eval.py

`run_eval.py` 的最小功能：

1. 读取 `golden.jsonl`。
2. 为每条 case 生成一个回答。
3. 写入 `runs/run-001.jsonl`。
4. 写入 `logs/run-001.log.jsonl`。

教学阶段可以先使用 mock：

```python
def mock_answer(case):
    return "这是一个教学用模拟回答，请根据 expected_points 人工评分。"
```

等流程跑通后，再替换为真实模型调用。真实调用时必须通过环境变量读取 API Key，不要写进代码或配置文件。

### 第 4 步：实现 score.py

评分可以分三层：

1. 人工评分：最适合初学者理解质量标准。
2. 规则评分：检查 expected points 命中情况。
3. LLM-as-Judge：作为辅助，不应完全替代人工抽检。

建议输出：

- `score`：0-5。
- `passed`：是否达到通过线，例如 score >= 4。
- `hallucination`：是否出现无依据内容。
- `safety_pass`：是否通过安全检查。
- `feedback`：一句改进建议。

### 第 5 步：实现 report.py

报告至少包含：

- run id、模型、prompt 版本。
- 用例总数。
- 平均分。
- 通过率。
- 安全通过率。
- 幻觉率。
- 平均延迟。
- token 总量。
- 失败用例表格。
- 高风险问题和下一步建议。

报告示例结构：

```md
# Eval Report: run-001

## Summary

## Metrics

## Failed Cases

## Security Findings

## Cost and Latency

## Recommendations
```

### 第 6 步：增加安全检查

在 `checklists/security.md` 中检查：

- 是否拒绝泄露系统提示词。
- 是否拒绝输出 API Key 或 token。
- 是否识别“不可信上下文中的指令”。
- 是否避免建议用户执行危险命令。
- 是否对高风险操作要求人工确认。

### 第 7 步：配置示例

在 `configs/eval.config.example.json` 中写教学配置：

```json
{
  "run_id": "run-001",
  "model": "mock-model",
  "prompt_version": "app_prompt_v1",
  "pass_score": 4,
  "dataset_path": "datasets/golden.jsonl",
  "output_path": "runs/run-001.jsonl",
  "log_path": "logs/run-001.log.jsonl",
  "report_path": "reports/run-001-report.md"
}
```

不要出现 `api_key` 的真实值。如需说明，使用环境变量名：`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等。

## 验收方式

### 必须通过

- [ ] `golden.jsonl` 至少 20 条，并覆盖正常、边界、安全样例。
- [ ] 每条 case 有 expected points。
- [ ] `run_eval.py` 能生成 run 文件和 log 文件，哪怕使用 mock answer。
- [ ] `score.py` 能写入或更新 score、passed、safety_pass。
- [ ] `report.py` 能生成 Markdown 报告。
- [ ] 日志不包含真实密钥、cookie、token 或未脱敏隐私。
- [ ] 报告列出失败用例和改进建议。

### 加分项

- [ ] 支持按 category 统计分数。
- [ ] 支持对比两个 run 的指标变化。
- [ ] 支持安全样例单独统计。
- [ ] 支持 CI 中运行小规模回归评测。
- [ ] 支持人工评分和 LLM-as-Judge 结果并存。

## 课堂演示建议

1. 先让学生只看 3 条样例，讨论“模型好不好”为什么难判断。
2. 再引入 golden dataset，让评价变得可复现。
3. 然后加入 run/log/report，展示一次 prompt 修改前后的对比。
4. 最后加入安全样例，说明高平均分不代表系统安全。

## 常见误区

- 只测正常问题，不测边界和攻击样例。
- expected points 写得太空，导致无法评分。
- 只看平均分，不看失败用例。
- 把 LLM-as-Judge 当成绝对真理。
- 日志中记录完整用户输入或真实密钥。
- 报告只有数字，没有改进建议。
