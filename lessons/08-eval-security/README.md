# 08 Eval / Security / Monitoring

## 学习目标

让 AI 应用从 Demo 走向可用系统，具备评测、监控、安全和成本意识。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习实验工程](04-exercises-lab/README.md)
- [实战项目](05-project.md)
- [项目实验工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)

## 核心概念

- Eval 评测
- Golden Dataset
- Eval Rubric
- Regression Set
- LLM-as-Judge
- 人工评审
- Token / Latency / Cost
- Prompt Injection
- Jailbreak
- 权限控制
- 监控和日志
- Safety Cases
- Red Team Samples

## 学习任务

1. 为一个 AI 应用设计测试集。
2. 记录模型输入、输出和评分。
3. 统计 token、延迟和成本。
4. 识别 Prompt Injection 风险。
5. 为工具调用设计权限控制。
6. 编写 0-5 分 eval rubric，明确通过线。
7. 建立回归集，覆盖正常、边界、幻觉和安全样例。
8. 将安全样例单独统计，避免平均分掩盖高风险失败。

## 进阶路线

评测体系建议按三层建设：

1. Rubric：明确什么是 0-5 分、什么算通过、什么必须失败。
2. Regression Set：固定一批每次改 prompt、模型、RAG 或 Agent 逻辑都要跑的样例。
3. Safety Set：单独维护 prompt injection、密钥泄露、高风险工具、隐私和越权样例。

报告中不要只展示平均分。至少同时展示：通过率、幻觉率、安全通过率、失败用例、成本、延迟和相对上一次 run 的变化。

## 实战项目

做一个 AI 应用评测面板。
