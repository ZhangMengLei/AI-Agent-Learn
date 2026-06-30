# 07 Claude Code 练习实验工程

本目录用于把 `03-exercises.md` 中的概念练习落到一个可操作的小工程里。练习目标不是“让 Claude Code 自动完成一切”，而是让你学会为 CLI Agent 提供清晰上下文、可复用命令、安全边界和自动化检查。

## 你将练习什么

完成本实验后，你应该能够：

- 为一个项目编写项目级 `CLAUDE.md`。
- 设计 1 个 slash command 的任务说明。
- 设计 1 个 hook 的触发条件和失败处理方式。
- 区分 settings 中的允许、确认和禁止操作。
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
    hooks/
      format-after-edit.json
    settings.example.json
  answers/
    README.md
```

说明：

- `starter/`：模拟一个很小的业务项目，用来练习让 Agent 读代码、改代码、跑测试。
- `workspace/`：学习者自己的实验产物，包含 `CLAUDE.md`、命令、hooks 和 settings 示例。
- `answers/`：参考答案说明。不要把它当作唯一标准答案，重点看设计理由。

如果你只是阅读课程，可以不真正创建全部文件；如果你要完成实验，建议按结构创建并逐步补齐。

## 练习任务

### 练习 1：编写项目级 CLAUDE.md

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
```

### 练习 2：设计 slash command

在 `workspace/commands/study-next.md` 中设计 `/study-next`：

- 输入：当前学习阶段、学习者自评、可用时间。
- 步骤：读取当前阶段 README、总结已学内容、推荐下一步练习。
- 输出：今日学习目标、练习清单、检查问题。

在 `workspace/commands/implement-small-change.md` 中设计 `/implement-small-change`：

- 输入：一个小需求，例如“给 calculator 增加除法”。
- 步骤：搜索代码、阅读测试、制定计划、修改代码、运行测试、总结变更。
- 边界：不要自动提交，不要改无关文件。

### 练习 3：设计 hook

在 `workspace/hooks/format-after-edit.json` 中写一个教学版 hook 配置。你不需要保证它能在所有环境直接运行，但要说明：

- 触发时机：例如编辑 JS 文件后。
- 执行动作：运行格式化或 lint。
- 失败处理：只报告错误，不自动删除或回滚文件。

示例思路：

```json
{
  "name": "format-after-edit",
  "event": "PostToolUse",
  "match": {
    "tool": "Edit",
    "path": "**/*.js"
  },
  "command": "npm run format -- --check",
  "on_failure": "show_error_and_stop"
}
```

实际 Claude Code hook schema 可能随版本变化；教学重点是理解触发条件、命令和失败策略。

### 练习 4：设计 settings 权限策略

在 `workspace/settings.example.json` 中写一个“教学版 settings 示例”，把操作分成三类：

| 类别 | 示例 | 原则 |
| --- | --- | --- |
| 可自动允许 | 读取文件、列目录、运行单元测试 | 低风险、只读或可重复执行 |
| 需要确认 | 安装依赖、修改配置、运行构建 | 可能改变环境或耗时 |
| 禁止自动执行 | 删除文件、force push、输出密钥 | 可能造成数据丢失或泄密 |

注意：不要把真实 token、真实 API Key、内网地址写入 settings。

### 练习 5：一次完整演练

用自然语言模拟一次 Claude Code 任务：

```text
请阅读 sample-project，为 calculator 增加 divide(a, b)，除数为 0 时返回错误，并补充测试。不要提交 git。
```

记录 Agent 应该如何执行：

1. 先读 `CLAUDE.md`。
2. 搜索 `calculator` 相关代码和测试。
3. 给出实现计划。
4. 修改代码和测试。
5. 运行测试。
6. 总结变更和未完成事项。

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
- 一个 hook 配置示例。
- 一份 settings 权限策略说明。
- 对“为什么这样设计”的解释。

评分时不要只看格式是否相同，更要看：

- Agent 是否知道项目边界。
- 高风险操作是否需要人工确认。
- 命令是否可重复、可检查。
- 输出是否便于人类复盘。

## 自检清单

- [ ] `CLAUDE.md` 包含项目规则、测试命令、安全注意事项。
- [ ] slash command 有输入、步骤、输出格式。
- [ ] hook 说明了触发条件、执行命令和失败处理。
- [ ] settings 示例不包含真实密钥。
- [ ] 权限策略没有自动允许删除、提交、推送等高风险动作。
- [ ] 能用 5 分钟向同学解释这个工作流如何运行。
