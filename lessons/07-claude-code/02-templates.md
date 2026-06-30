# Claude Code 常用模板

本节提供可直接复制改造的教学模板。模板不是越长越好，而是要让 Agent 明确：上下文是什么、可以做什么、不能做什么、如何验证、如何汇报。

## 1. `CLAUDE.md` 模板

```markdown
# Project Guide

## 项目简介

本项目是一个示例 Web 应用，用于演示功能开发、测试和代码审查流程。

## 技术栈

- 语言：JavaScript / TypeScript / Python，按真实项目填写
- 包管理：npm / pnpm / pip，按真实项目填写
- 测试：Jest / Vitest / unittest，按真实项目填写

## 常用命令

- 安装依赖：`npm install`
- 启动开发：`npm run dev`
- 运行测试：`npm test`
- 类型检查：`npm run typecheck`
- 格式化检查：`npm run format -- --check`

## 修改规则

1. 修改代码前先搜索相关实现和测试。
2. 优先阅读最小必要文件，不要无目的扫全仓库。
3. 每次只改与当前任务直接相关的文件。
4. 复杂改动先给计划，等待用户确认后再执行。
5. 新增行为必须补充或更新测试。

## 安全边界

- 不要读取、输出、提交真实 API Key、密码、cookie、token。
- 不要自动执行 `git commit`、`git push`、`git reset --hard`、`git push --force`。
- 删除文件、安装依赖、修改 CI/CD、访问网络或生产系统前必须询问用户。
- 不要绕过测试、hooks 或 review 要求。

## 输出要求

任务结束时请输出：

1. 修改文件。
2. 运行过的验证命令和结果。
3. 未验证事项。
4. 风险和后续建议。
```

## 2. Slash Command 模板

适合放在类似 `.claude/commands/implement-feature.md` 的位置。

```markdown
# /implement-feature

请在当前仓库中实现一个小型功能，并补充必要测试。

## 输入

- 用户需求：$ARGUMENTS
- 限制：不要自动提交 git；不要修改无关文件；如需安装依赖先询问。

## 步骤

1. 阅读 `CLAUDE.md`，提取项目规则和测试命令。
2. 复述需求，列出不明确点；如需求不清晰，先提问。
3. 搜索相关代码和测试。
4. 阅读最小必要文件。
5. 输出修改计划、影响范围、验证方式和风险点。
6. 等待用户确认后再修改。
7. 修改代码和测试。
8. 运行相关测试或轻量检查。
9. 查看 diff，确认没有无关修改。
10. 输出最终总结。

## 输出格式

## 需求理解
## 修改计划
## 执行结果
## 验证结果
## 风险与后续建议
```

## 3. Skill 模板

适合放在类似 `.claude/skills/safe-feature/SKILL.md` 的位置。不同版本 Claude Code 的真实目录和加载方式可能有差异，教学重点是理解 Skill 的组成：触发描述、流程、工具规则和边界。

```markdown
---
name: safe-feature
description: 当用户要求在当前仓库实现小型功能、补充测试、运行本地验证并总结变更时使用。若任务涉及删除文件、安装依赖、访问网络、git commit、git push、生产环境或真实密钥，必须先询问用户。
---

# Safe Feature Skill

## 何时使用

- 用户要求修复 bug、实现小功能、补测试、做小范围重构。
- 用户希望 Agent 在仓库中实际编辑文件并验证。

## 不适用场景

- 只需要概念解释。
- 涉及生产数据、真实密钥、发布上线或不可逆操作。
- 需求范围过大，无法在一次任务中安全完成。

## 工作流程

1. 读取项目规则：优先查看 `CLAUDE.md` 和 README。
2. 确认需求：复述目标、范围和禁止事项。
3. 搜索代码：定位实现、测试和配置。
4. 制定计划：说明文件、步骤、验证命令和风险。
5. 等待确认：复杂或高风险修改必须先确认。
6. 执行修改：小步编辑，避免无关文件。
7. 验证：运行测试、lint 或 compile 检查。
8. 总结：报告修改文件、验证结果、未完成事项。

## 工具和权限规则

- 允许：读取文件、搜索代码、查看 git diff、运行本地测试。
- 询问：安装依赖、修改配置、运行长耗时命令、创建提交。
- 禁止自动执行：删除目录、force push、输出密钥、修改生产数据。

## 输出格式

- 修改文件：
- 验证命令：
- 验证结果：
- 风险：
- 需要用户确认或合并的事项：
```

### Skill description 写法对比

不推荐：

```markdown
description: 写代码时使用。
```

推荐：

```markdown
description: 当用户要求扫描当前仓库、实现小型功能、补测试并运行本地验证时使用；遇到删除、提交、推送、联网、生产环境或密钥相关操作必须先询问。
```

原因：好的描述同时说明触发条件、任务范围和安全边界。

## 4. Hook 配置思路

教学版“编辑后检查”示例：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run format -- --check"
          }
        ]
      }
    ]
  }
}
```

设计 hook 时要写清楚：

- 触发事件：例如编辑文件后。
- 匹配范围：例如只匹配 `src/**/*.ts`。
- 执行动作：例如格式化检查、lint、单元测试。
- 失败处理：停止后续自动执行，向用户报告错误。

不要把 hook 设计成自动删除、自动提交、自动推送。Hook 的默认职责应是检查和提醒。

## 5. Settings / Permissions 模板

教学版示例，不要复制真实个人配置，不要写真实 token。

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(python -m compileall:*)",
      "Bash(npm test:*)"
    ],
    "ask": [
      "Bash(npm install:*)",
      "Bash(pip install:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(rm -rf:*)",
      "Bash(git reset --hard:*)"
    ]
  }
}
```

初学者只需要掌握原则：

- allow：低风险、只读、可重复验证。
- ask：改变环境、历史或外部系统。
- deny：不可逆、泄密、生产写入、绕过安全流程。

## 6. Subagents 拆分模板

```markdown
# 子 Agent 拆分方案

## 背景

目标：为当前仓库完成一次功能修改和审查。

## 子任务

1. 代码定位 Agent
   - 搜索入口、调用链和相关测试。
   - 输出涉及文件和理由。

2. 测试分析 Agent
   - 阅读现有测试。
   - 判断需要新增或更新哪些用例。

3. 安全检查 Agent
   - 检查是否涉及密钥、权限、删除、网络、生产环境。
   - 输出 BLOCK / WARN / PASS。

4. 总结 Agent
   - 根据主 Agent 确认后的事实整理最终说明。

## 汇总规则

主 Agent 必须统一判断多个子 Agent 的结论；冲突点要说明，不能直接拼接结果。
```

## 7. Plan Mode 输出模板

```markdown
## 需求理解

- 用户要完成什么：
- 明确限制：
- 需要澄清的问题：

## 计划

1. 阅读文件：
2. 搜索关键词：
3. 修改范围：
4. 验证命令：
5. 回滚或风险处理：

## 风险

- 可能影响的模块：
- 可能失败的测试：
- 需要用户确认的操作：

请确认是否按此计划执行。
```

## 8. Worktree 操作提示模板

当用户要求在独立 worktree 中工作时，最终总结建议包含：

```markdown
## Worktree 结果

- 工作目录：/absolute/path/to/worktree
- 修改文件：
- 验证结果：
- 未提交变更：是/否
- 需要主会话合并的路径：/absolute/path/to/worktree
```

这样主会话可以明确知道从哪里检查 diff、运行验证和合并改动。

## 9. Code Review 输出模板

```markdown
## Summary

- 本次变更做了什么。

## Findings

### BLOCK

- 必须修复的问题，例如安全漏洞、测试失败、数据丢失风险。

### WARN

- 建议修复的问题，例如边界条件、可维护性、缺少测试。

### PASS

- 已检查且未发现问题的范围。

## Test Plan

- 已执行或建议执行的测试。

## Risk

- 发布、兼容性、权限、数据和安全风险。
```
