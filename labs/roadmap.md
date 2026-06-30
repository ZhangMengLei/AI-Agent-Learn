# 学习进度表

本文用于帮助你按阶段推进 AI Agent 学习。你可以复制本表到自己的笔记中，记录完成情况、问题和下一步计划。

## 总体路线

| 阶段 | 主题 | 核心产物 | 状态 |
| --- | --- | --- | --- |
| 01 | Prompt | 提示词模板和对比记录 | 未开始 |
| 02 | LLM API | 最小 API 调用和错误处理 | 未开始 |
| 03 | Tool Use | 工具调用 schema 和执行记录 | 未开始 |
| 04 | RAG | 文档切分、检索、问答流程 | 未开始 |
| 05 | Agent | 规划、工具调用、状态管理 | 未开始 |
| 06 | MCP | MCP Server/Client 基础实验 | 未开始 |
| 07 | Claude Code | CLAUDE.md、slash command、hooks、settings | 未开始 |
| 08 | Eval / Security | golden dataset、评分、日志、报告 | 未开始 |

## 每阶段完成标准

建议每个阶段都完成：

- [ ] 阅读 `README.md`。
- [ ] 阅读 `01-basic.md`。
- [ ] 阅读 `02-templates.md`。
- [ ] 完成 `03-exercises.md`。
- [ ] 完成 `04-exercises-lab/README.md` 中的核心练习。
- [ ] 完成 `05-project.md`。
- [ ] 完成 `06-project-lab/README.md` 中的项目方案或最小实现。
- [ ] 阅读 `07-review.md` 并自评。

## 进阶主线：从 Mock 到真实 API，再到可评测系统

完成基础 8 个阶段后，建议按下面路线补强工程能力：

1. LLM API 替换路径：保留 mock provider，抽象真实 provider，使用 env 控制 provider / model / timeout / retry。
2. RAG 进阶：从关键词检索升级到 embedding、vector store、hybrid search、rerank 和 retrieval eval。
3. Agent 进阶：把 state 持久化，支持 checkpoint / resume / failure recovery，输出可观测 trace 日志。
4. Eval / Security 进阶：建立 rubric、regression set、安全样例和趋势报告。

这条主线的目标是：每个 demo 都能回答“如何安全切换真实 API”“如何排障”“如何评测是否变好或变坏”。

## 02 LLM API 进阶进度

| 任务 | 完成情况 | 备注 |
| --- | --- | --- |
| 保留 mock provider | 未完成 | 默认不访问真实 API |
| 设计 provider 抽象 | 未完成 | generate / stream 统一接口 |
| 设计 env 配置 | 未完成 | provider、model、key env、timeout、retry |
| 实现 streaming partial output 处理 | 未完成 | 中途失败不能当成功 |
| 实现错误分类 | 未完成 | missing_key、auth、rate_limit、timeout 等 |
| 完成真实 API smoke test | 未完成 | 只在本机显式开启，不提交密钥 |

## 04 RAG 进阶进度

| 任务 | 完成情况 | 备注 |
| --- | --- | --- |
| chunk metadata 完整 | 未完成 | source、section、line、hash |
| embedding 封装 | 未完成 | mock 可替换真实 embedding |
| vector store 可重建 | 未完成 | 删除后可完整重建 |
| hybrid search | 未完成 | 关键词 + 向量 |
| rerank | 未完成 | Top 20 到 Top 3-5 |
| retrieval eval | 未完成 | expected_sources、Top K 命中率、拒答率 |

## 05 Agent 进阶进度

| 任务 | 完成情况 | 备注 |
| --- | --- | --- |
| state schema | 未完成 | goal、plan、step、observations、logs |
| checkpoint 持久化 | 未完成 | 每轮迭代后保存 |
| resume 恢复 | 未完成 | 不重复已成功高风险动作 |
| failure recovery | 未完成 | retry / skip / stop / human confirm |
| trace 日志 | 未完成 | run_id、trace_id、phase、decision |
| 报告引用观察结果 | 未完成 | 结论可回溯 |

## 07 Claude Code 进度

| 任务 | 完成情况 | 备注 |
| --- | --- | --- |
| 理解 CLAUDE.md 作用 | 未完成 |  |
| 编写项目级 CLAUDE.md | 未完成 |  |
| 设计 slash command | 未完成 |  |
| 设计 hook | 未完成 |  |
| 设计 settings 权限策略 | 未完成 |  |
| 完成阶段复盘 | 未完成 |  |

## 08 Eval / Security 进度

| 任务 | 完成情况 | 备注 |
| --- | --- | --- |
| 设计 golden dataset | 未完成 | 正常、边界、幻觉、安全样例 |
| 编写评分 rubric | 未完成 | 0-5 分、通过线、rubric 版本 |
| 建立 regression set | 未完成 | prompt / 模型 / RAG / Agent 变更后复跑 |
| 维护 safety set | 未完成 | prompt injection、密钥泄露、越权工具 |
| 记录 run result | 未完成 | score、passed、safety_pass、hallucination |
| 设计脱敏日志 | 未完成 | 不记录 key、cookie、完整隐私输入 |
| 生成 Markdown 报告 | 未完成 | 平均分、通过率、安全通过率、失败用例 |
| 完成安全检查清单 | 未完成 | 高风险失败单独列出 |
| 完成阶段复盘 | 未完成 |  |

## 每周复盘问题

1. 本周我真正跑通了哪个最小流程？
2. 哪个概念我还能讲给别人听？
3. 哪个问题我只是照抄，还没有理解？
4. 我的实验中有没有真实密钥或隐私风险？
5. 下一周最小可完成目标是什么？

## 学习建议

- 不要跳过复盘。复盘能帮助你从“会操作”变成“会设计”。
- 不要只追求 demo 成功。AI 工程更重要的是可评测、可排障、可控风险。
- 不要把所有任务都交给 Agent。初学阶段要能解释每一步为什么这样做。
