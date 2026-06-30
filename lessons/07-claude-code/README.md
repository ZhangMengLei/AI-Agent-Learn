# 07 Claude Code / CLI / Skill

## 学习目标

掌握 CLI Agent 在真实软件工程中的用法，包括读代码、改代码、跑测试、配置工具、设计 Skill、隔离工作区和自动化流程。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习实验工程](04-exercises-lab/README.md)
- [Skill 专项实验](skill-lab/README.md)
- [实战项目](05-project.md)
- [项目实验工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)

## 核心概念

- Claude Code CLI
- `CLAUDE.md`
- Slash Commands
- Skills
- Skill 触发描述和目录结构
- Hooks
- Settings
- Permissions
- MCP 集成
- Subagents
- Plan Mode
- Worktree
- 安全边界

## 学习任务

1. 理解 CLI Agent 能做什么、不能自动做什么。
2. 编写项目级 `CLAUDE.md`。
3. 理解 slash command 和 Skill 的区别。
4. 设计一个包含触发描述、流程和安全边界的 Skill。
5. 配置一个简单 hook，并说明失败处理。
6. 设计 settings / permissions 权限分层。
7. 了解 MCP 如何接入 Claude Code。
8. 使用 plan mode 处理复杂任务。
9. 判断何时使用 worktree 隔离改动。
10. 用 subagents 拆分复杂搜索、审查和总结任务。

## 实战项目

做一个 Claude Code 自动化工作流：用 `CLAUDE.md`、slash command、Skill、hooks、settings、plan mode 和 worktree 组合出可复用、可验证、可控的工程助手。
