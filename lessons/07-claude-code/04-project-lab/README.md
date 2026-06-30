# 07 Claude Code 项目实验工程

本项目实验要求你设计一个“Claude Code 自动化工程助手”工作流。它不追求复杂功能，而是训练你把 `CLAUDE.md`、slash command、hooks 和 settings 组合成一个清晰、安全、可复用的教学工程。

## 项目目标

构建一个面向小型代码仓库的 Claude Code 工作流，使 Agent 能够在人工监督下完成：

1. 阅读需求。
2. 理解项目规则。
3. 搜索和阅读相关代码。
4. 制定修改计划。
5. 修改代码并运行测试。
6. 进行基础代码审查。
7. 输出变更总结。

本项目不要求调用真实线上服务，不要求提交 git，不要求连接生产环境。

## 推荐文件结构

请在 `04-project-lab/` 下实现以下结构：

```text
04-project-lab/
  README.md
  claude-workflow/
    CLAUDE.md
    commands/
      implement-feature.md
      review-change.md
      summarize-work.md
      create-test-plan.md
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

目录说明：

- `CLAUDE.md`：项目级上下文和行为规则，是 Agent 的“工程说明书”。
- `commands/`：把常见工作流沉淀成 slash command 文档。
- `hooks/`：说明自动化检查在何时触发、执行什么、失败怎么办。
- `settings.example.json`：教学版权限配置示例，只写占位符和原则，不写真实密钥。
- `sample-tasks/`：给学习者演练的需求样例。
- `checklists/`：人工验收和复盘清单。

## 实现步骤

### 第 1 步：定义工程边界

在 `claude-workflow/CLAUDE.md` 中写清楚：

- 这个仓库的技术栈假设。
- 常用命令，例如测试、lint、格式化。
- 允许 Agent 自动做什么。
- 哪些操作必须询问用户。
- 禁止输出或记录任何真实 API Key、密码、cookie、token。
- 不要自动提交 git，除非用户明确要求。

建议规则：

```md
## 工作原则

1. 先理解，再修改。
2. 先计划，再执行。
3. 每次只改与任务直接相关的文件。
4. 所有高风险操作都必须等待用户确认。
5. 任务结束时说明修改文件、测试结果和风险。
```

### 第 2 步：设计 `/implement-feature`

在 `commands/implement-feature.md` 中描述一个完整功能开发流程：

1. 读取 `CLAUDE.md`。
2. 复述用户需求和限制。
3. 搜索相关代码。
4. 阅读最小必要文件。
5. 输出实现计划。
6. 等待用户确认。
7. 修改代码和测试。
8. 运行测试。
9. 总结结果。

输出格式建议：

```md
## 需求理解
## 修改计划
## 风险点
## 执行结果
## 测试结果
## 后续建议
```

### 第 3 步：设计 `/review-change`

在 `commands/review-change.md` 中设计代码审查流程，重点检查：

- 是否修改了无关文件。
- 是否缺少测试。
- 是否引入密钥泄露风险。
- 是否有破坏性命令或危险配置。
- 是否需要更新文档。

### 第 4 步：设计 hooks

在 `hooks/lint-after-edit.json` 中描述“编辑后检查”：

- 触发：编辑源代码文件后。
- 动作：运行 lint 或格式化检查。
- 失败：停止后续自动执行并提示错误。

在 `hooks/test-before-summary.json` 中描述“总结前测试”：

- 触发：准备输出最终总结前。
- 动作：运行相关测试。
- 失败：总结中必须明确说明测试失败，不允许假装通过。

注意：本课程中的 hook 文件是教学方案，不要求和某个版本的真实 schema 完全一致。你需要能解释它的触发条件和安全意义。

### 第 5 步：设计 settings 权限策略

在 `settings.example.json` 中给出示例策略：

- 允许：只读搜索、读取文件、运行测试、查看 git diff。
- 询问：安装依赖、修改构建配置、创建提交、访问网络。
- 禁止：force push、删除目录、输出密钥、修改生产数据。

不要复制真实个人配置。settings 示例中只能出现占位符和教学命令。

### 第 6 步：准备演练任务

在 `sample-tasks/task-001-form-validation.md` 中写一个小需求：

```text
为登录表单增加邮箱格式校验，错误时展示提示文案，并补充测试。不要提交 git。
```

在 `sample-tasks/task-002-refactor-naming.md` 中写一个重构需求：

```text
把 userInfo 相关变量统一改为 userProfile，保持行为不变，并运行测试。不要改无关文件。
```

### 第 7 步：编写验收清单

在 `checklists/` 下准备三类清单：

- `pre-change.md`：动手前是否理解需求、范围和风险。
- `post-change.md`：改完后是否跑测试、看 diff、总结结果。
- `safety.md`：是否避免密钥、删除、推送、生产操作等风险。

## 验收方式

项目完成后，用下面标准验收：

### 必须通过

- [ ] 有可读的 `CLAUDE.md`，包含命令、规则、安全边界。
- [ ] 至少有 3 个 slash command 设计。
- [ ] 至少有 2 个 hook 设计。
- [ ] 有 settings 权限策略示例，且不包含真实密钥。
- [ ] 有至少 2 个 sample task 可用于课堂演练。
- [ ] 有改前、改后、安全三类检查清单。

### 加分项

- [ ] slash command 输出格式统一，适合复制到课堂使用。
- [ ] hooks 能说明失败时如何阻断风险。
- [ ] settings 能区分“低风险自动化”和“高风险人工确认”。
- [ ] 项目说明中明确“不提交 git、不删除文件、不连接生产”。

## 课堂演示建议

1. 教师先展示一个没有 `CLAUDE.md` 的任务，让学生观察 Agent 容易遗漏什么。
2. 再加入 `CLAUDE.md` 和 slash command，对比输出是否更稳定。
3. 最后加入 hook 和 settings，讨论自动化与安全边界。

## 常见误区

- 把 slash command 写成一句简单提示，缺少步骤和输出格式。
- 在 settings 示例中写入真实路径、真实 token 或个人配置。
- hook 只写“运行测试”，但不说明失败后怎么办。
- 让 Agent 自动 commit 或 push，忽略人工确认。
- CLAUDE.md 写得过长，但缺少真正可执行的命令和规则。
