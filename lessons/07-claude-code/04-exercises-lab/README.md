# 07 Claude Code 练习实验工程

本目录用于把 `03-exercises.md` 中的概念练习落到一个可操作的小工程里。练习目标不是“让 Claude Code 自动完成一切”，而是让你学会为 CLI Agent 提供清晰上下文、可复用命令、安全边界和自动化检查。

## 你将练习什么

完成本实验后，你应该能够：

- 为一个项目编写项目级 `CLAUDE.md`。
- 设计 1 个 slash command 的任务说明。
- 设计 1 个 Skill 的触发描述、流程和安全边界。
- 设计 1 个 hook 的触发条件和失败处理方式。
- 区分 settings 中的允许、确认和禁止操作。
- 用 plan mode 先制定方案，再执行可控修改。
- 判断何时应该使用独立 worktree。
- 用复盘清单判断一个 Claude Code 工作流是否安全、可解释、可复用。

## 建议目录

请在本目录下按下面结构完成练习文件：

```text
04-exercises-lab/
  README.md
  starter/
    sample-project/
      README.md
      src/
        calculator.js
      tests/
        calculator.test.js
  workspace/
    CLAUDE.md
    commands/
      study-next.md
      implement-small-change.md
    skills/
      safe-feature/
        SKILL.md
        examples/
          request.md
    hooks/
      format-after-edit.json
    settings.example.json
    run-log.md
  answers/
    README.md
```

说明：

- `starter/`：模拟一个很小的业务项目，用来练习让 Agent 读代码、改代码、跑测试。
- `workspace/`：学习者自己的实验产物，包含 `CLAUDE.md`、命令、Skill、hooks 和 settings 示例。
- `answers/`：参考答案说明。不要把它当作唯一标准答案，重点看设计理由。

如果你只是阅读课程，可以不真正创建全部文件；如果你要完成实验，建议按结构创建并逐步补齐。

## 练习任务

### 练习 1：编写项目级 `CLAUDE.md`

在 `workspace/CLAUDE.md` 中写入以下内容：

1. 项目简介：这个 sample project 是什么。
2. 常用命令：如何安装依赖、运行测试、格式化代码。
3. 修改规则：改代码前需要先读哪些文件。
4. 安全规则：哪些命令不能自动执行。
5. 输出要求：任务完成后如何总结。

建议包含这类规则：

```md
- 修改代码前先说明计划。
- 不要自动提交 git。
- 不要读取或输出真实密钥。
- 删除文件、推送代码、修改 CI 配置前必须询问用户。
- 任务结束时报告修改文件、验证命令、验证结果和未完成事项。
```

### 练习 2：设计 slash command

在 `workspace/commands/study-next.md` 中设计 `/study-next`：

- 输入：当前学习阶段、学习者自评、可用时间。
- 步骤：读取当前阶段 README、总结已学内容、推荐下一步练习。
- 输出：今日学习目标、练习清单、检查问题。
- 边界：不要自动修改课程文件，除非用户明确要求。

在 `workspace/commands/implement-small-change.md` 中设计 `/implement-small-change`：

- 输入：一个小需求，例如“给 calculator 增加除法”。
- 步骤：读取 `CLAUDE.md`、搜索代码、阅读测试、制定计划、等待确认、修改代码、运行测试、总结变更。
- 边界：不要自动提交，不要改无关文件；安装依赖、删除文件、访问网络前必须询问。

### 练习 3：设计 Skill

在 `workspace/skills/safe-feature/SKILL.md` 中写一个教学版 Skill。它应该包含 frontmatter 和正文。

示例骨架：

```md
---
name: safe-feature
description: 当用户要求在当前仓库实现小型功能、修复 bug、补充测试并运行本地验证时使用。若涉及删除文件、安装依赖、访问网络、git commit、git push、生产环境或真实密钥，必须先询问用户。
---

# Safe Feature Skill

## 何时使用

## 不适用场景

## 工作流程

## 工具和权限规则

## 安全边界

## 输出格式
```

要求：

- `description` 不能只写“帮助写代码”。
- 必须说明触发条件和不适用场景。
- 必须说明哪些操作允许、哪些询问、哪些禁止。
- 必须规定最终输出格式。

在 `workspace/skills/safe-feature/examples/request.md` 中写一个好请求和一个坏请求，例如：

```md
好请求：请在当前 sample project 中为 calculator 增加 divide(a, b)，除数为 0 时抛出错误，并补充测试。不要提交 git。

坏请求：直接帮我改项目，顺便推送到远端。
```

### 练习 4：设计 hook

在 `workspace/hooks/format-after-edit.json` 中写一个教学版 hook 配置。你不需要保证它能在所有环境直接运行，但要说明：

- 触发时机：例如编辑 JS 文件后。
- 执行动作：运行格式化或 lint。
- 失败处理：只报告错误，不自动删除、不回滚、不提交。

示例思路：

```json
{
  "name": "format-after-edit",
  "event": "PostToolUse",
  "match": {
    "tool": "Edit",
    "path": "src/**/*.js"
  },
  "command": "npm run format -- --check",
  "on_failure": "show_error_and_stop"
}
```

实际 Claude Code hook schema 可能随版本变化；教学重点是理解触发条件、命令和失败策略。

### 练习 5：设计 settings 权限策略

在 `workspace/settings.example.json` 中写一个“教学版 settings 示例”，把操作分成三类：

| 类别 | 示例 | 原则 |
| --- | --- | --- |
| 可自动允许 | 读取文件、列目录、运行单元测试、查看 git diff | 低风险、只读或可重复执行 |
| 需要确认 | 安装依赖、修改配置、创建提交、访问网络 | 可能改变环境、历史或外部系统 |
| 禁止自动执行 | 删除目录、force push、输出密钥、修改生产数据 | 可能造成数据丢失或泄密 |

教学版 JSON 可以写成：

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(npm test:*)"
    ],
    "ask": [
      "Bash(npm install:*)",
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

注意：不要把真实 token、真实 API Key、内网地址写入 settings。

### 练习 6：Plan Mode 演练

先不要修改代码，只在 `workspace/run-log.md` 中写计划：

```text
请阅读 sample-project，为 calculator 增加 divide(a, b)，除数为 0 时抛出错误，并补充测试。不要提交 git。
```

计划必须包含：

1. 需求理解。
2. 要阅读的文件。
3. 要搜索的关键词。
4. 修改范围。
5. 测试命令。
6. 风险点。
7. 需要用户确认的问题。

### 练习 7：一次完整演练

用自然语言模拟一次 Claude Code 任务，并把执行记录追加到 `workspace/run-log.md`：

```text
请阅读 sample-project，为 calculator 增加 divide(a, b)，除数为 0 时抛出错误，并补充测试。不要提交 git。
```

记录 Agent 应该如何执行：

1. 先读 `CLAUDE.md`。
2. 搜索 `calculator` 相关代码和测试。
3. 给出实现计划。
4. 等待确认后修改代码和测试。
5. 运行测试。
6. 查看 diff，确认没有无关修改。
7. 总结变更和未完成事项。

### 练习 8：Worktree 判断

回答以下问题并写入 `workspace/run-log.md`：

- 当前任务是否适合独立 worktree？为什么？
- 如果在 worktree 中完成，最终报告应该包含哪些绝对路径？
- 哪些文件或配置不应该复制到 worktree 或提交？

建议最终报告格式：

```md
## Worktree 结果

- 工作目录：/absolute/path/to/worktree
- 修改文件：
- 验证结果：
- 需要主会话合并的路径：/absolute/path/to/worktree
```

## 运行/使用方式

这是教学实验，不强制绑定某个语言栈。推荐使用以下方式：

```bash
# 进入你创建的 sample project
cd lessons/07-claude-code/04-exercises-lab/starter/sample-project

# 如果你选择 JavaScript 示例，可安装依赖并运行测试
npm install
npm test
```

如果你没有真实 sample project，也可以只完成 `workspace/` 下的文档设计，并用伪代码说明测试命令。

## 参考答案说明

参考答案建议放在 `answers/README.md`，包含：

- 一份可读的 `CLAUDE.md` 示例。
- 两个 slash command 的示例内容。
- 一个 Skill 示例，包含触发描述和安全边界。
- 一个 hook 配置示例。
- 一份 settings 权限策略说明。
- 一份 plan mode 和 worktree 演练记录。
- 对“为什么这样设计”的解释。

评分时不要只看格式是否相同，更要看：

- Agent 是否知道项目边界。
- Skill 是否能准确触发，且不会越权执行。
- 高风险操作是否需要人工确认。
- 命令是否可重复、可检查。
- 输出是否便于人类复盘。

## 自检清单

- [ ] `CLAUDE.md` 包含项目规则、测试命令、安全注意事项。
- [ ] slash command 有输入、步骤、输出格式。
- [ ] Skill 有明确 description、适用场景、不适用场景和安全边界。
- [ ] hook 说明了触发条件、执行命令和失败处理。
- [ ] settings 示例不包含真实密钥。
- [ ] 权限策略没有自动允许删除、提交、推送等高风险动作。
- [ ] plan mode 记录包含文件、命令、风险和验收方式。
- [ ] worktree 记录包含需要主会话合并的绝对路径。
- [ ] 能用 5 分钟向同学解释这个工作流如何运行。
