# 01 Prompt Engineering

## 学习目标

掌握如何清晰地向大模型描述任务，让模型输出更稳定、可控、可复用。

## 学习内容

- [Prompt 基础](01-basic.md)
- [Prompt 模板示例](02-templates.md)
- [Prompt 练习](03-exercises.md)
- [Prompt 练习工程](03-exercises-lab/README.md)
- [Prompt 实战项目](04-project.md)
- [Prompt 项目工程](04-project-lab/README.md)
- [Prompt 阶段复盘](05-review.md)

## 核心概念

- System Prompt / Developer Prompt / User Prompt
- Zero-shot / Few-shot
- 角色、任务、背景、约束、示例
- 输出格式控制：Markdown、JSON、表格
- Prompt Chaining
- ReAct：Reason + Act
- 幻觉与边界控制

## 学习任务

1. 写一个总结文章的 Prompt。
2. 写一个代码解释 Prompt。
3. 写一个固定输出 JSON 的 Prompt。
4. 对同一个任务测试 3 种不同 Prompt，比较效果。

## 实战项目

做一个 `Prompt 模板库`，包含：

- 总结
- 翻译
- 代码解释
- 需求分析
- SQL 生成
- 测试用例生成

## 检查标准

- Prompt 是否包含清晰任务？
- 是否说明输出格式？
- 是否给了必要上下文？
- 是否限制模型不要编造？
