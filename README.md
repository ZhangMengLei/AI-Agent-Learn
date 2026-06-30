# AI-Agent-Learn

从零开始学习 AI、LLM 与 Agent 工程化实践的路线仓库。

## 学习目标

本仓库按从简单到深入的顺序，系统学习：

- Prompt Engineering
- LLM API / SDK
- Tool Use / Function Calling
- RAG 知识库问答
- Agent 架构
- MCP（Model Context Protocol）
- Claude Code / CLI Agent / Skill / Hook
- Eval、监控与安全

## 推荐学习顺序

```text
Prompt
  ↓
LLM API
  ↓
Tool Use / Function Calling
  ↓
RAG
  ↓
Agent
  ↓
MCP
  ↓
Claude Code / CLI / Skill
  ↓
Eval / Security / Deployment
```

## 目录结构

```text
lessons/
  01-prompt/
    README.md          阶段说明
    01-basic.md        讲解：基础概念
    02-templates.md    模板：可复用 Prompt
    03-exercises.md    练习：动手任务
  02-llm-api/          LLM API 与 SDK
  03-tool-use/         工具调用与 Function Calling
  04-rag/              RAG 知识库问答
  05-agent/            Agent 架构与任务循环
  06-mcp/              MCP 协议与 Server 开发
  07-claude-code/      Claude Code、CLI、Skill、Hook
  08-eval-security/    评测、监控与安全
```

## 每个阶段的组织方式

后续每个阶段都尽量按这个结构整理：

```text
README.md              阶段目标和学习路径
01-basic.md            讲解：核心概念
02-templates.md        模板：可复用写法或配置
03-exercises.md        练习：动手任务
04-project.md          项目：小实战
```

## 阶段学习入口

1. [Prompt Engineering](lessons/01-prompt/README.md)
2. [LLM API 与 SDK](lessons/02-llm-api/README.md)
3. [Tool Use / Function Calling](lessons/03-tool-use/README.md)
4. [RAG 知识库问答](lessons/04-rag/README.md)
5. [Agent 架构](lessons/05-agent/README.md)
6. [MCP](lessons/06-mcp/README.md)
7. [Claude Code / CLI / Skill](lessons/07-claude-code/README.md)
8. [Eval / Security](lessons/08-eval-security/README.md)

## 建议实战项目

按难度递增：

1. Prompt 模板库
2. 命令行 AI 聊天助手
3. PDF / 文档知识库问答
4. 工具调用 Agent
5. 代码修复 Agent
6. MCP Server
7. Claude Code 自动化工作流

## 学习原则

- 先理解概念，再写最小 Demo。
- 每学一个阶段，都做一个可运行的小项目。
- 不只关注“模型回答”，更要关注工具、上下文、权限、评测和安全。
- Agent 不是魔法，本质是：目标拆解、工具调用、观察结果、持续推进。
