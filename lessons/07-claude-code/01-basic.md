# Claude Code / CLI / Skill 基础

## CLI Agent 是什么

CLI Agent 是运行在命令行里的 AI Agent。

它不仅能聊天，还可以在你的项目中：

- 阅读文件
- 搜索代码
- 修改代码
- 运行测试
- 查看 Git 状态
- 生成提交说明
- 调用外部工具
- 使用 MCP Server

## Claude Code 是什么

Claude Code 是面向软件工程任务的 CLI Agent。

它适合做：

- 解释陌生代码库
- 修复 bug
- 添加测试
- 重构代码
- 代码审查
- 安全审查
- 自动化重复流程

## CLAUDE.md

`CLAUDE.md` 是给 Claude Code 的项目说明。

可以写：

- 项目介绍
- 常用命令
- 测试方式
- 代码规范
- 注意事项
- 不要做的事情

它相当于项目里的协作说明书。

## Slash Commands

Slash Command 是固定工作流入口。

例如：

```text
/review
/test
/security-review
```

适合把常用任务变成可重复执行的命令。

## Skills

Skill 是更完整的能力包，通常包含：

- 使用场景
- 操作流程
- 工具调用方式
- 约束和注意事项

适合封装专业任务，例如 PR review、安全审查、文档处理。

## Hooks

Hooks 是在特定事件前后自动执行的命令。

例如：

- 编辑后自动格式化
- 提交前运行测试
- 停止时发送提醒
- 工具调用前做检查

## Settings 和 Permissions

Settings 用于配置 Claude Code 行为。

Permissions 用于控制哪些命令或工具可以执行，哪些需要确认。

## MCP 集成

Claude Code 可以通过 MCP 接入外部工具和数据源。

例如：

- GitHub
- 数据库
- 文档系统
- 内部 API

## Subagents

Subagents 可以把复杂任务拆给多个子 Agent 做。

适合：

- 并行搜索不同模块
- 独立审查代码
- 生成不同主题文档

## Plan Mode

Plan Mode 适合复杂改动。

先让 Agent 阅读项目、制定计划，再经过用户确认后执行。

## Worktree

Worktree 用于隔离开发环境，避免影响当前工作区。

适合多个任务并行开发。

## 一句话总结

Claude Code 把 Agent 能力放进真实工程流程里，让 AI 可以读代码、改代码、跑测试和自动化协作。
