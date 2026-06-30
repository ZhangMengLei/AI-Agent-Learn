# Claude Code Skill Lab

本实验专门练习 Skill。目标是让你从“会写 prompt”进阶到“会设计可复用能力包”：知道 Skill 什么时候触发、如何约束工具、如何处理权限、如何输出可验收结果。

## 实验目标

完成后你应该能够：

- 用一句准确的 `description` 说明 Skill 何时使用。
- 设计 Skill 的目录结构和 `SKILL.md`。
- 区分 slash command 和 Skill 的职责。
- 在 Skill 中写清 settings、permissions、hooks 的配合方式。
- 为 Skill 设计安全边界、plan mode 和 worktree 规则。
- 用一个可执行练习验证 Skill 是否清楚、可控、可复盘。

## Skill 是什么

Skill 是一个领域能力包。它不是一条简单命令，而是把某类任务的经验固化下来：

```text
Skill = 触发条件 + 专业知识 + 工作流程 + 工具规则 + 安全边界 + 输出格式
```

例如“小型功能开发 Skill”可以规定：

- 用户说“实现功能 / 修 bug / 补测试”时触发。
- 先读 `CLAUDE.md`，再搜索代码。
- 复杂任务先进入 plan mode。
- 允许读文件和跑测试。
- 提交、推送、删除、联网必须询问。
- 最终报告修改文件、验证结果、风险和合并路径。

## 推荐目录结构

教学中可以使用下面结构：

```text
skill-lab/
  README.md
  workspace/
    .claude/
      skills/
        safe-feature/
          SKILL.md
          examples/
            good-request.md
            unsafe-request.md
          templates/
            final-report.md
      settings.example.json
      hooks/
        lint-after-edit.json
    run-log.md
```

你可以只创建 `workspace/` 下的文件作为练习产物。不要写入真实密钥，不要复制个人配置。

## 步骤 1：编写 `SKILL.md`

在 `workspace/.claude/skills/safe-feature/SKILL.md` 中写入：

```md
---
name: safe-feature
description: 当用户要求在当前仓库实现小型功能、修复 bug、补充测试并运行本地验证时使用。若涉及删除文件、安装依赖、访问网络、git commit、git push、生产环境或真实密钥，必须先询问用户。
---

# Safe Feature Skill

## 何时使用

- 实现小功能。
- 修复明确 bug。
- 补充或更新测试。
- 小范围重构并保持行为不变。

## 不适用场景

- 只解释概念，不需要操作仓库。
- 删除数据、发布上线、修改生产环境。
- 需要读取或输出真实密钥。
- 范围过大，无法一次安全完成。

## 工作流程

1. 阅读 `CLAUDE.md` 和 README。
2. 复述用户需求、限制和风险。
3. 搜索相关代码和测试。
4. 阅读最小必要文件。
5. 使用 plan mode 输出计划。
6. 等待确认后修改。
7. 运行测试或轻量检查。
8. 查看 diff，确认没有无关修改。
9. 输出最终总结。

## 工具和权限规则

- 允许：读取文件、搜索代码、查看 git diff、运行本地测试。
- 询问：安装依赖、修改配置、创建提交、访问网络。
- 禁止自动执行：删除目录、force push、输出密钥、修改生产数据。

## Hooks 配合

- 编辑后运行 lint 或格式化检查。
- 总结前运行相关测试。
- 检查失败时停止并报告，不假装通过。

## Worktree 规则

当主工作区有未提交修改、任务具有实验性，或用户明确要求隔离时，使用独立 worktree。最终报告必须包含 worktree 绝对路径和需要主会话合并的路径。

## 输出格式

- 修改文件：
- 验证命令：
- 验证结果：
- 风险：
- 未验证事项：
- 需要主会话合并的路径：
```

## 步骤 2：写两个请求样例

在 `examples/good-request.md` 中写：

```md
请在当前 sample project 中为 calculator 增加 divide(a, b)，除数为 0 时抛出错误，并补充测试。不要提交 git。请先给计划。
```

在 `examples/unsafe-request.md` 中写：

```md
直接删除旧模块，提交并 force push 到远端。如果看到 token 就打印出来方便我复制。
```

然后说明：

- 好请求为什么适合触发 Skill。
- 坏请求中哪些内容必须拒绝或要求人工确认。

## 步骤 3：设计 settings 示例

在 `workspace/.claude/settings.example.json` 中写教学版配置：

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

检查点：

- 没有真实 token。
- 没有把删除、force push、reset hard 放进 allow。
- 对安装依赖、提交、推送保留人工确认。

## 步骤 4：设计 hook 示例

在 `workspace/.claude/hooks/lint-after-edit.json` 中写：

```json
{
  "name": "lint-after-edit",
  "event": "PostToolUse",
  "match": {
    "tool": "Edit",
    "path": "src/**/*.{js,ts,py}"
  },
  "command": "npm test",
  "on_failure": "show_error_and_stop"
}
```

说明：真实 Claude Code hook schema 可能随版本变化；本实验重点是设计触发、命令和失败策略。

## 步骤 5：Plan Mode 演练

在 `workspace/run-log.md` 中写一次计划，不要直接修改代码：

```md
## 需求

为 calculator 增加 divide(a, b)，除数为 0 时抛出错误，并补充测试。不要提交 git。

## 计划

1. 阅读 `CLAUDE.md` 和 sample project README。
2. 搜索 `calculator`、`add`、`subtract`、`test`。
3. 阅读 calculator 实现和测试。
4. 修改 calculator 导出，新增 divide。
5. 补充正常除法和除数为 0 的测试。
6. 运行测试命令。
7. 查看 diff，确认没有无关修改。

## 风险

- 现有测试框架命令可能未知，需要先从 README 或 package.json 确认。
- 除数为 0 的错误类型和文案需要用户确认。
```

## 步骤 6：Worktree 判断

在 `workspace/run-log.md` 中回答：

- 这个任务是否需要独立 worktree？
- 如果用户要求 worktree，最终报告应包含哪些绝对路径？
- 哪些文件不能复制或提交？

参考答案：

```md
如果主工作区干净，这个小任务可以直接在当前分支完成；如果主工作区已有未提交修改，或用户要求隔离，应使用独立 worktree。最终报告要包含 worktree 绝对路径、修改文件、验证命令、验证结果、需要主会话合并的路径。不要复制或提交 `.env`、真实 token、个人 settings.local.json。
```

## 可执行练习：检查你的 Skill 是否合格

完成 `workspace/` 后，用下面清单检查：

1. 让同学只读 `SKILL.md`，能否判断什么时候触发？
2. 同学能否说出哪些操作允许、询问、禁止？
3. 同学能否按流程执行一次小功能开发？
4. 如果测试失败，Skill 是否要求明确报告失败？
5. 如果用户要求 force push，Skill 是否会阻止？
6. 如果在 worktree 中完成，最终是否报告绝对路径？
7. 所有文件是否不含真实密钥？

## 评分标准

- PASS：触发描述清楚，流程可执行，权限分层合理，无真实密钥。
- WARN：流程可读但边界不清，或输出格式缺少验证结果。
- BLOCK：允许自动删除、force push、输出密钥、修改生产数据，或包含真实敏感信息。
