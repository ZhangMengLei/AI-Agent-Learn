# Labs 学习支持文档

`labs/` 用来承载本课程所有教学实验的通用说明。每个阶段的 `04-exercises-lab` 和 `06-project-lab` 会给出具体任务，本目录提供跨阶段都适用的环境、安全和排障指南。

## 推荐阅读顺序

### 通用入门顺序

1. [environment.md](environment.md)：准备本地学习环境。
2. [api-key-guide.md](api-key-guide.md)：理解 API Key 安全和环境变量使用方式。
3. [../lessons/00-ai-foundation/README.md](../lessons/00-ai-foundation/README.md)：先建立 AI、LLM、Agent、RAG、MCP 的整体认知。
4. [troubleshooting.md](troubleshooting.md)：遇到依赖、运行、权限、模型调用问题时排查。
5. [roadmap.md](roadmap.md)：按阶段记录学习进度。

### 常见开发中使用 AI 的顺序

如果你是小白，想先把 AI 用到日常开发任务中，推荐按下面顺序阅读：

1. [environment.md](environment.md)：确认本地命令、编辑器和 Python 环境可用。
2. [api-key-guide.md](api-key-guide.md)：先建立密钥和敏感信息边界，避免把真实 Key 写进仓库。
3. [roadmap.md#开发实战周日常开发使用-ai](roadmap.md#开发实战周日常开发使用-ai)：按 5 天节奏完成需求澄清、读代码、实现、测试、Review 和排障练习。
4. [developer-ai-workflows.md](developer-ai-workflows.md)：学习常见开发场景下如何给 AI 上下文、拆任务、检查结果。
5. [developer-prompt-recipes.md](developer-prompt-recipes.md)：复制常用 Prompt Recipes，完成自己的第一个小需求或 Bug 修复。
6. [troubleshooting.md](troubleshooting.md)：当 AI 输出不可运行、依赖报错或权限不清晰时回到这里排查。

## Labs 的学习方式

建议每个阶段都按下面节奏完成：

1. **先读理论**：阅读阶段 `01-basic.md` 和 `02-templates.md`。
2. **完成练习**：阅读 `03-exercises.md`，再到 `04-exercises-lab/` 完成工程化练习。
3. **完成项目**：阅读 `05-project.md`，再到 `06-project-lab/` 设计或实现小项目。
4. **阶段复盘**：阅读 `07-review.md`，用检查清单自评。
5. **记录问题**：把卡住的问题写在自己的学习笔记里，下一次优先解决。

## 通用目录约定

每个阶段推荐包含：

```text
lessons/<stage>/
  README.md
  01-basic.md
  02-templates.md
  03-exercises.md
  04-exercises-lab/
    README.md
  05-project.md
  06-project-lab/
    README.md
  07-review.md
```

说明：

- `04-exercises-lab/`：偏小练习，目标是理解一个技能点。
- `06-project-lab/`：偏综合项目，目标是把多个技能组合起来。
- `07-review.md`：阶段复盘、常见错误和检查清单。

## 学习原则

- 不要在仓库中写入真实 API Key、密码、cookie、token。
- 不要把生产数据复制到学习实验中。
- 不要在不理解命令含义时执行删除、推送、覆盖等高风险操作。
- 先用 mock 数据跑通流程，再接入真实模型。
- 先追求可解释、可复盘，再追求自动化。

## 适合初学者的完成标准

一个 lab 不需要一次做到完美，只要满足：

- 能说明它解决什么问题。
- 有清晰输入和输出。
- 有最小可运行或可演示流程。
- 有基本安全边界。
- 有复盘记录和下一步改进方向。

## 和 07、08 阶段的关系

- [developer-ai-workflows.md](developer-ai-workflows.md)：把 07 阶段的 CLI Agent 能力落到需求澄清、读代码、实现、测试、Review、排障等日常开发流程中。
- [developer-prompt-recipes.md](developer-prompt-recipes.md)：把 Prompt、Tool Use、Claude Code 的常见开发提示词模板整理成可复用清单。
- `07-claude-code`：重点练习 `CLAUDE.md`、slash command、hooks、settings，把 Agent 工作流工程化。
- `08-eval-security`：重点练习 golden dataset、评分、日志、报告和安全样例，把 AI 应用质量评测工程化。
