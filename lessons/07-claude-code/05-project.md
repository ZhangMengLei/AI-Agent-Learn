# Claude Code 实战项目：自动化工作流与 Skill

## 项目目标

设计一套 Claude Code 工作流，用来处理一个常见软件工程任务：阅读需求、理解项目规则、制定计划、修改代码、运行测试、审查风险、总结变更。

本项目的重点不是“让 AI 自动做完所有事”，而是训练你把 Agent 能力放进可控工程流程中：

- 用 `CLAUDE.md` 提供稳定上下文。
- 用 slash command 固化常见流程。
- 用 Skill 封装专业任务和安全边界。
- 用 settings / permissions 控制工具权限。
- 用 hooks 在关键时机自动检查。
- 用 plan mode 避免盲目修改。
- 用 worktree 隔离实验性改动。
- 用 subagents 拆分复杂审查任务。

## 工作流场景

示例任务：

```text
为项目添加一个表单校验功能，并补充测试。不要自动提交 git。
```

推荐执行流程：

```text
接收需求
  ↓
读取 CLAUDE.md 和项目 README
  ↓
识别是否命中 Skill
  ↓
搜索相关代码和测试
  ↓
进入 plan mode 制定实现计划
  ↓
用户确认
  ↓
在当前工作区或独立 worktree 中修改
  ↓
运行测试、lint 或轻量检查
  ↓
必要时调用 review / security 子流程
  ↓
输出总结和合并路径
```

## 推荐项目文件

```text
claude-workflow/
  CLAUDE.md
  commands/
    implement-feature.md
    review-change.md
    summarize-work.md
    create-test-plan.md
  skills/
    safe-feature/
      SKILL.md
      examples/
        form-validation-request.md
        unsafe-request.md
    safe-review/
      SKILL.md
  hooks/
    lint-after-edit.json
    test-before-summary.json
  settings.example.json
  sample-tasks/
    task-001-form-validation.md
    task-002-refactor-naming.md
  checklists/
    pre-change.md
    post-change.md
    safety.md
```

## 必备内容

### 1. `CLAUDE.md`

说明项目规则、测试命令、注意事项。它至少应该回答：

- 项目是什么，主要目录在哪里？
- 常用测试、lint、格式化命令是什么？
- 修改代码前必须阅读哪些文件？
- 哪些操作可以自动执行？
- 哪些操作必须询问用户？
- 哪些操作禁止自动执行？
- 任务结束时如何汇报？

示例规则：

```md
## 工作原则

1. 先理解，再修改。
2. 先计划，再执行。
3. 每次只改与任务直接相关的文件。
4. 删除文件、安装依赖、提交、推送、访问网络前必须询问用户。
5. 禁止输出真实 API Key、密码、cookie、token。
6. 任务结束时说明修改文件、验证结果、风险和未完成事项。
```

### 2. Slash Command

设计一个 `/implement-feature` 工作流。它应该包含：

- 输入：用户需求和限制。
- 步骤：读规则、搜代码、读测试、计划、确认、修改、验证、总结。
- 输出：需求理解、修改计划、风险、执行结果、测试结果。
- 边界：不要自动提交，不要改无关文件，不要访问生产环境。

再设计 `/review-change` 和 `/summarize-work`，分别用于代码审查和最终汇报。

### 3. Skill

设计一个 `safe-feature` Skill，专门处理“小型功能开发 + 补测试 + 本地验证”。

`SKILL.md` 至少包含：

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

设计要点：

- `description` 必须具体，不能只写“帮助写代码”。
- 写清楚触发词，例如“实现功能”“修复 bug”“补测试”“运行验证”。
- 写清楚不适用场景，例如生产操作、真实密钥、发布上线、不可逆删除。
- 写清楚工具规则，例如允许读文件和跑测试，提交和推送必须确认。
- 写清楚验收方式，例如测试命令、diff 检查、最终总结。

### 4. Hook

设计至少两个 hook：

1. 编辑后检查：编辑源代码文件后运行 lint 或格式化检查。
2. 总结前测试：准备最终总结前运行相关测试，失败时必须报告。

Hook 文件要说明：

- 触发时机。
- 匹配范围。
- 执行命令。
- 失败处理。
- 安全意义。

不要让 hook 自动执行删除、提交、推送或生产写入。

### 5. 权限策略

在 `settings.example.json` 中说明哪些操作允许自动执行、哪些需要确认、哪些禁止。

建议策略：

| 分类 | 操作 | 理由 |
| --- | --- | --- |
| 允许 | 读取文件、搜索代码、查看 git diff、运行单元测试 | 低风险、可复盘 |
| 询问 | 安装依赖、修改配置、创建提交、访问网络 | 改变环境或外部状态 |
| 禁止 | force push、删除目录、输出密钥、修改生产数据 | 不可逆或可能泄密 |

### 6. Subagents 拆分

为复杂任务设计 subagents 拆分方案：

```text
主 Agent
  ├─ 代码定位 Agent：找入口、调用链、测试
  ├─ 测试 Agent：判断覆盖缺口
  ├─ 安全 Agent：检查密钥、权限、危险命令
  └─ 文档 Agent：整理总结和使用说明
```

要求：主 Agent 必须汇总和判断子 Agent 的发现，不能直接把结果拼接给用户。

### 7. Plan Mode

在复杂任务中必须先计划。计划至少包含：

- 需求理解。
- 要阅读的文件。
- 修改范围。
- 验证命令。
- 风险点。
- 需要用户确认的问题。

示例输出：

```md
## 计划

1. 阅读 `CLAUDE.md` 和表单模块 README。
2. 搜索 `login`、`email`、`validation`。
3. 修改登录表单校验逻辑和相关测试。
4. 运行 `npm test -- login`。
5. 风险：可能影响现有错误提示文案。

请确认是否按此计划执行。
```

### 8. Worktree

当用户要求隔离环境，或主工作区已有未提交修改时，应考虑使用独立 worktree。

最终报告必须包含：

- worktree 绝对路径。
- 修改文件。
- 验证命令和结果。
- 是否有未提交变更。
- 需要主会话合并的路径。

## 验收标准

- 有清晰 `CLAUDE.md`。
- 有至少 3 个 slash command 设计。
- 有至少 1 个 Skill 设计。
- 有至少 2 个 hook 设计。
- 有 settings 权限策略说明。
- 能说明 subagents 如何拆分复杂任务。
- 能说明 plan mode 何时使用、计划里包含什么。
- 能说明 worktree 何时使用、如何报告合并路径。
- 没有真实密钥、真实 token、个人隐私配置。
- 能说明完整工作流如何运行。

## 扩展方向

- 接入 MCP Server，但必须先说明权限和数据边界。
- 增加代码审查工作流。
- 增加安全审查工作流。
- 增加 PR 自动总结工作流。
- 增加课程专用 Skill，让学生一键检查自己的实验产物。
