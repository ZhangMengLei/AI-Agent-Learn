# 07 Claude Code / CLI / Skill

## 学习目标

掌握 CLI Agent 在真实软件工程中的用法，包括读代码、改代码、跑测试、配置工具和自动化流程。

## 核心概念

- Claude Code CLI
- CLAUDE.md
- Slash Commands
- Skills
- Hooks
- Settings
- Permissions
- MCP 集成
- Subagents
- Plan Mode
- Worktree

## Claude Code 能做什么

- 解释代码
- 修改代码
- 运行测试
- 搜索项目
- 创建提交
- 创建 PR
- 代码审查
- 安全审查
- 自动化重复工作流

## 学习任务

1. 在一个项目中运行 Claude Code。
2. 让 Claude Code 阅读并解释代码结构。
3. 编写项目级 `CLAUDE.md`。
4. 使用 slash command 完成固定流程。
5. 配置一个 MCP Server。
6. 了解 Skill 如何封装专用能力。
7. 配置简单 Hook，例如编辑后格式化或测试前检查。

## 实战项目

做一个 `Claude Code 自动化工作流`：

- 自动阅读需求
- 制定实现计划
- 修改代码
- 运行测试
- 生成变更总结

## 注意事项

- 高风险操作需要人工确认。
- 不要让 Agent 随意删除文件或重置 Git。
- 让 Agent 先计划，再执行复杂任务。
- 对生成代码要跑测试和人工 review。
