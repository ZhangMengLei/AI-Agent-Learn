# Implementations 可运行实现总览

本目录放置课程中的可运行参考实现。它们优先使用 Python 标准库和 mock 数据，目标是帮助学习者理解工程结构，而不是直接作为生产系统。

## 当前可运行 Demo

| 阶段 | 实现目录 | 运行命令 | 学习重点 | 是否写入文件 |
| --- | --- | --- | --- | --- |
| 01 Prompt | [01-prompt-lab](./01-prompt-lab/) | `make demo-prompt` | Prompt 模板、结构化质量检查、mock 输出 | 否 |
| 02 LLM API | [02-llm-chat](./02-llm-chat/) | `make demo-llm` | messages、streaming、多轮上下文、调用日志；进阶关注 provider/env 设计和真实 API 安全切换 | 否 |
| 03 Tool Use | [03-tool-assistant](./03-tool-assistant/) | `make demo-tool` | 工具注册、参数校验、权限确认、tool log | 否，默认内存演示 |
| 04 RAG | [04-rag-assistant](./04-rag-assistant/) | `make demo-rag QUERY="Agent 和 Chatbot 区别是什么"` | Markdown 加载、chunk、检索、引用；进阶关注 embedding、vector store、rerank、retrieval eval | 否 |
| 05 Agent | [05-research-agent](./05-research-agent/) | `make demo-agent` | 计划、工具调用、观察、报告生成；进阶关注 state checkpoint、失败恢复和 trace 日志 | 是，会覆盖 `runs/latest-report.md` |
| 06 MCP | [06-mcp-server](./06-mcp-server/) | `make demo-mcp` | JSON-RPC、tools、resources、prompts；进阶关注 stdio/SSE、客户端配置和调试 | 否 |
| 07 Claude Code | [07-claude-code-workflow](./07-claude-code-workflow/) | `make demo-claude-code` | CLI Agent 工作流、权限策略、hook 示例；进阶关注 Skill、settings、worktree 和 subagents | 否 |
| 08 Eval / Security | [08-eval-lab](./08-eval-lab/) | `make demo-eval` | golden dataset、规则评分、安全样例、报告；进阶关注 rubric、回归集和安全失败单独统计 | 是，会覆盖 `reports/run-001-report.md` |

## 真实 API 替换注意事项

当前实现以 mock 和本地数据为主，适合教学和离线验证。如果要把任一 demo 替换为真实 LLM API，请遵守：

1. 保留 mock provider，真实 provider 通过配置显式开启。
2. API Key 只从环境变量读取，配置文件只保存 `api_key_env`。
3. test / CI 环境不调用网络。
4. streaming 要处理 partial output，不把中途失败的回答当作完整成功。
5. 错误日志只记录 error_type、latency、model、token usage，不记录请求头或密钥。
6. RAG 真实 embedding 要记录 embedding model 和 content hash，保证索引可重建。
7. Agent 真实工具调用要先接入权限确认、checkpoint 和失败恢复。
8. Eval 报告要包含 rubric 版本、回归集结果和安全样例单独统计。

## 推荐学习方式

1. 先阅读对应阶段的 `lessons/<stage>/README.md`。
2. 再阅读实现目录中的 README。
3. 运行 demo，观察输入、输出和中间日志。
4. 对照 `solutions/<stage>/` 中的答案讲解，理解为什么这样设计。
5. 修改一个小点，例如增加样例数据、工具、评分规则或停止条件，再运行测试。

## 本地验证

```bash
make check
make demo-prompt
make demo-llm
make demo-tool
make demo-rag QUERY="RAG 为什么需要引用"
make demo-mcp
make demo-claude-code
```

说明：`make check` 只做编译、单元测试和密钥误提交检查，不运行会覆盖报告文件的 demo。完整体验 01-08 全阶段可以运行 `make demo-all`，其中 `demo-agent` 和 `demo-eval` 会覆盖本地报告文件。
