# AI-Agent-Learn

从零开始学习 AI、LLM 与 Agent 工程化实践的路线仓库。目标是把概念、模板、练习、项目、数据样例和自查清单放在同一个可运行的课程工程里，帮助学习者逐步完成从 Prompt 到 RAG、Agent、MCP、评测与安全的实践闭环。

## 适合谁

- 想系统学习 AI Agent 工程化，但不知道从哪里开始的开发者。
- 已经会写基础 Python，希望补齐 LLM API、工具调用、RAG、Agent 工作流的工程实践者。
- 需要把 AI 能力接入业务系统、知识库或自动化流程的后端、前端、测试、数据同学。
- 想用 Claude Code、MCP、自动化评测等能力提升研发效率的工程师。
- 准备设计内部 AI 课程、工作坊或团队学习路线的讲师与技术负责人。

## 如何开始

### 1. 准备环境

建议使用 Python 3.10+。

```bash
python -m venv .venv
source .venv/bin/activate
make install
```

如果暂时不想使用 Makefile，也可以直接执行：

```bash
python -m pip install -r requirements.txt
```

### 2. 配置环境变量

复制示例配置，不要把真实 API Key 提交到仓库。

```bash
cp .env.example .env
```

按需填写 `.env` 中的本地配置。课程中的示例默认以占位符展示，真实密钥只保存在本机环境变量或 `.env` 文件中。

### 3. 从总览进入课程

建议先阅读：

1. [labs/environment.md](labs/environment.md)：环境准备。
2. [labs/api-key-guide.md](labs/api-key-guide.md)：API Key 安全配置。
3. [labs/roadmap.md](labs/roadmap.md)：学习进度表。
4. [checkpoints/README.md](checkpoints/README.md)：阶段自查方式。
5. [lessons/00-ai-foundation/README.md](lessons/00-ai-foundation/README.md)：AI 基础导学，先理解 AI、LLM、Agent、RAG、MCP 的关系。

如果你是第一次接触 AI 开发、目标是先学会“常见开发中怎么用 AI”，可以直接从开发场景入口开始：

1. [labs/README.md](labs/README.md)：查看推荐阅读顺序。
2. [labs/roadmap.md#开发实战周日常开发使用-ai](labs/roadmap.md#开发实战周日常开发使用-ai)：按 1 周节奏练习日常开发使用 AI。
3. [labs/developer-ai-workflows.md](labs/developer-ai-workflows.md)：学习需求澄清、代码理解、实现、测试、Review、排障等开发工作流。
4. [labs/developer-prompt-recipes.md](labs/developer-prompt-recipes.md)：复制常用提示词模板，先在真实小任务中用起来。

## 五条学习路径

### 路径零：AI 基础导学

适合第一次接触 AI、LLM、Agent、RAG、MCP 等概念的学习者。

学习顺序：

1. [lessons/00-ai-foundation/README.md](lessons/00-ai-foundation/README.md)：建立 AI、机器学习、深度学习、大模型和 LLM 的整体认知。
2. [lessons/00-ai-foundation/01-basic.md](lessons/00-ai-foundation/01-basic.md)：理解 token、上下文窗口、幻觉、Chatbot、RAG、Agent、MCP 的直观含义。
3. [checkpoints/checkpoint-00-ai-foundation.md](checkpoints/checkpoint-00-ai-foundation.md)：完成基础自查。

建议目标：能用自己的话解释 AI / LLM / RAG / Agent / MCP 的区别，知道后续每个阶段解决什么问题。

### 路径一：快速入门

适合想在短时间内跑通最小 Demo、建立全局认知的学习者。

学习顺序：

1. [lessons/01-prompt/README.md](lessons/01-prompt/README.md)：理解 Prompt 的结构化表达。
2. [lessons/02-llm-api/README.md](lessons/02-llm-api/README.md)：了解如何通过 API 调用模型。
3. [lessons/03-tool-use/README.md](lessons/03-tool-use/README.md)：理解模型如何选择和调用工具。
4. [checkpoints/checkpoint-01-prompt.md](checkpoints/checkpoint-01-prompt.md) 到 [checkpoints/checkpoint-03-tool-use.md](checkpoints/checkpoint-03-tool-use.md)：完成基础自查。

建议目标：能写出清晰 Prompt，能解释一次 LLM API 调用包含哪些输入输出，能设计一个简单工具调用流程。

### 路径二：知识库 / RAG

适合想做企业文档问答、知识库检索、客服辅助、学习资料问答的学习者。

学习顺序：

1. 先完成快速入门路径中的 Prompt 与 LLM API 基础。
2. [lessons/04-rag/README.md](lessons/04-rag/README.md)：学习切分、向量化、召回、重排、生成。
3. [data/docs/](data/docs/)：使用样例文档作为本地知识库材料。
4. [data/eval/golden.jsonl](data/eval/golden.jsonl)：用黄金集检查问答效果。
5. [checkpoints/checkpoint-04-rag.md](checkpoints/checkpoint-04-rag.md)：完成 RAG 自查。

建议目标：能从本地 Markdown 文档构建一个最小知识库问答 Demo，并能用固定问题集评估效果。

### 路径三：工程 Agent

适合想做自动化任务执行、研发助手、工具编排、多步骤工作流的学习者。

学习顺序：

1. 完成 Prompt、LLM API、Tool Use 基础。
2. [lessons/05-agent/README.md](lessons/05-agent/README.md)：学习 Agent 的目标、计划、行动、观察循环。
3. [lessons/06-mcp/README.md](lessons/06-mcp/README.md)：学习 MCP 如何标准化工具和上下文接入。
4. [lessons/07-claude-code/README.md](lessons/07-claude-code/README.md)：学习 CLI Agent、Skill、Hook 等工程协作方式。
5. [lessons/08-eval-security/README.md](lessons/08-eval-security/README.md)：补齐评测、安全、权限和上线前检查。
6. [checkpoints/checkpoint-05-agent.md](checkpoints/checkpoint-05-agent.md) 到 [checkpoints/checkpoint-08-eval-security.md](checkpoints/checkpoint-08-eval-security.md)：完成工程化自查。

建议目标：能设计一个有边界、有权限、有日志、有评测的自动化 Agent，而不是只依赖模型自由发挥。

### 路径四：日常开发使用 AI

适合想先把 AI 用到需求理解、读代码、写实现、补测试、Code Review 和排障中的初学者。

学习顺序：

1. [labs/README.md](labs/README.md)：先按 Labs 推荐阅读顺序完成环境、安全和排障准备。
2. [labs/roadmap.md#开发实战周日常开发使用-ai](labs/roadmap.md#开发实战周日常开发使用-ai)：按“开发实战周”安排每天的小任务。
3. [labs/developer-ai-workflows.md](labs/developer-ai-workflows.md)：学习常见开发工作流中如何拆任务、给上下文、验收输出。
4. [labs/developer-prompt-recipes.md](labs/developer-prompt-recipes.md)：使用现成提示词模板完成第一个小需求或 Bug 修复。
5. 回到 [lessons/01-prompt/README.md](lessons/01-prompt/README.md)、[lessons/03-tool-use/README.md](lessons/03-tool-use/README.md)、[lessons/07-claude-code/README.md](lessons/07-claude-code/README.md)，补齐提示词、工具调用和 CLI Agent 基础。

建议目标：能在不提交真实密钥、不复制生产敏感数据的前提下，用 AI 辅助完成一个可解释、可检查、可回滚的小型开发任务。

## 每阶段学习顺序说明

每个阶段都采用同一套结构，建议按顺序学习：

1. `README.md`：先看阶段目标、学习路径和产出物。
2. `01-basic.md`：理解核心概念，明确这个阶段解决什么问题。
3. `02-templates.md`：学习可复用模板，沉淀提示词、代码结构或配置结构。
4. `03-exercises.md`：完成小练习，验证是否真正理解概念。
5. `04-exercises-lab/`：进入练习工程，把单点能力变成可运行实验。
6. `05-project.md`：阅读阶段项目说明，理解真实场景需求。
7. `06-project-lab/`：完成项目工程，形成可展示成果。
8. `07-review.md`：复盘常见错误、质量标准和下一步优化方向。
9. `checkpoints/`：最后用自查问题确认是否可以进入下一阶段。

## 如何运行 demos

当前仓库不强制绑定某一家模型服务。可运行实现默认使用 Python 标准库和 mock 数据，适合先理解工程结构，再逐步替换为真实模型服务。

先查看可用命令：

```bash
make help
make install
make list
make check
```

### 当前可运行实现

| 阶段 | 实现目录 | 运行命令 | 学习重点 |
| --- | --- | --- | --- |
| 01 Prompt | [implementations/01-prompt-lab](implementations/01-prompt-lab/) | `make demo-prompt` | Prompt 模板、结构化质量检查、mock 输出 |
| 02 LLM API | [implementations/02-llm-chat](implementations/02-llm-chat/) | `make demo-llm` | messages、streaming、多轮上下文、调用日志 |
| 03 Tool Use | [implementations/03-tool-assistant](implementations/03-tool-assistant/) | `make demo-tool` | 工具注册、参数校验、权限确认、tool log |
| 04 RAG | [implementations/04-rag-assistant](implementations/04-rag-assistant/) | `make demo-rag QUERY="Agent 和 Chatbot 区别是什么"` | Markdown 加载、chunk、检索、引用 |
| 05 Agent | [implementations/05-research-agent](implementations/05-research-agent/) | `make demo-agent` | 计划、工具调用、观察、报告生成 |
| 06 MCP | [implementations/06-mcp-server](implementations/06-mcp-server/) | `make demo-mcp` | JSON-RPC、tools、resources、prompts |
| 07 Claude Code | [implementations/07-claude-code-workflow](implementations/07-claude-code-workflow/) | `make demo-claude-code` | CLI Agent 工作流、权限策略、hook 示例 |
| 08 Eval / Security | [implementations/08-eval-lab](implementations/08-eval-lab/) | `make demo-eval` | golden dataset、规则评分、安全样例、报告 |

说明：

- `lessons/` 是主课程路径，包含讲解、模板、练习、项目和复盘。
- `implementations/` 是可运行参考工程，帮助你把概念跑起来。
- `solutions/` 是做完练习后的答案讲解，不建议一开始就看。
- `make demo-agent` 和 `make demo-eval` 会生成或覆盖本地报告文件。
- 新增 01/02/06/07 demo 默认只打印输出，不写入文件。
- 使用真实模型服务前，请先配置 `.env`，并确认 `.gitignore` 已忽略 `.env`。

也可以使用 Makefile 中的通用 lesson 入口：

```bash
make demo STAGE=01-prompt LAB=04-exercises-lab
make demo STAGE=04-rag LAB=06-project-lab
```

如果目标 lesson 目录还只是课程说明，请按对应 `README.md` 完成练习。对于 RAG 练习，可优先使用 [data/docs/](data/docs/) 和 [data/eval/golden.jsonl](data/eval/golden.jsonl) 作为样例输入。

## 答案与讲解

完成练习后可以查看 [solutions/README.md](solutions/README.md)。答案目录按课程阶段组织，覆盖：

- `03-exercises.md`：每个练习的参考答案、原因和常见错误。
- `04-exercises-lab.md`：练习工程参考流程和验收标准。
- `05-project.md`：项目设计讲解和评分标准。
- `06-project-lab.md`：项目实现路线、测试方式和扩展方向。

## 目录结构

```text
lessons/
  00-ai-foundation/          AI 基础导学
  01-prompt/                 Prompt Engineering
  02-llm-api/                LLM API 与 SDK
  03-tool-use/               Tool Use / Function Calling
  04-rag/                    RAG 知识库问答
  05-agent/                  Agent 架构
  06-mcp/                    MCP
  07-claude-code/            Claude Code / CLI / Skill
  08-eval-security/          Eval / Security
labs/
  README.md                  全局实验说明与推荐阅读顺序
  environment.md             环境准备
  api-key-guide.md           API Key 安全配置
  troubleshooting.md         常见问题排查
  roadmap.md                 学习进度表
  developer-ai-workflows.md  日常开发使用 AI 的工作流
  developer-prompt-recipes.md 常见开发提示词模板
data/
  docs/                      RAG 与知识库样例文档
  notes/                     结构化学习笔记样例
  eval/                      评测黄金集样例
implementations/             01-08 全阶段可运行参考实现
tests/                       unittest 自动化测试
checkpoints/                 每阶段自查问题
solutions/                   参考答案、讲解和项目复盘
```

## 阶段学习入口

0. [AI 基础导学](lessons/00-ai-foundation/README.md)
1. [Prompt Engineering](lessons/01-prompt/README.md)
2. [LLM API 与 SDK](lessons/02-llm-api/README.md)
3. [Tool Use / Function Calling](lessons/03-tool-use/README.md)
4. [RAG 知识库问答](lessons/04-rag/README.md)
5. [Agent 架构](lessons/05-agent/README.md)
6. [MCP](lessons/06-mcp/README.md)
7. [Claude Code / CLI / Skill](lessons/07-claude-code/README.md)
8. [Eval / Security](lessons/08-eval-security/README.md)

## 开发场景学习入口

如果你想先解决“常见开发中怎么使用 AI”，从这里进入：

1. [开发实战周 / 日常开发使用 AI](labs/roadmap.md#开发实战周日常开发使用-ai)：把学习拆成 5 个可执行日任务。
2. [日常开发 AI 工作流](labs/developer-ai-workflows.md)：覆盖需求澄清、代码阅读、实现、测试、Review、排障。
3. [开发提示词模板](labs/developer-prompt-recipes.md)：沉淀可复制的 Prompt Recipes。

## 建议实战项目

按难度递增：

1. Prompt 模板库。
2. 命令行 AI 聊天助手。
3. PDF / Markdown 文档知识库问答。
4. 工具调用 Agent。
5. 代码修复 Agent。
6. MCP Server。
7. Claude Code 自动化工作流。
8. 带评测、安全检查和日志追踪的工程 Agent。

## 学习原则

- 先理解概念，再写最小 Demo。
- 每学一个阶段，都做一个可运行的小项目。
- 不只关注“模型回答”，更要关注工具、上下文、权限、评测和安全。
- Agent 不是魔法，本质是：目标拆解、工具调用、观察结果、持续推进。
- 不提交真实 API Key，不把敏感数据放进样例数据和评测集。
