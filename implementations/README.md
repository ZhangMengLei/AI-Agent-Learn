# Implementations 可运行实现总览

本目录放置课程中的可运行参考实现。它们优先使用 Python 标准库和 mock 数据，目标是帮助学习者理解工程结构，而不是直接作为生产系统。

## 当前可运行 Demo

| 阶段 | 实现目录 | 运行命令 | 学习重点 | 是否写入文件 |
| --- | --- | --- | --- | --- |
| 03 Tool Use | [03-tool-assistant](./03-tool-assistant/) | `make demo-tool` | 工具注册、参数校验、权限确认、tool log | 否，默认内存演示 |
| 04 RAG | [04-rag-assistant](./04-rag-assistant/) | `make demo-rag QUERY="Agent 和 Chatbot 区别是什么"` | Markdown 加载、chunk、检索、引用 | 否 |
| 05 Agent | [05-research-agent](./05-research-agent/) | `make demo-agent` | 计划、工具调用、观察、报告生成 | 是，会覆盖 `runs/latest-report.md` |
| 08 Eval / Security | [08-eval-lab](./08-eval-lab/) | `make demo-eval` | golden dataset、规则评分、安全样例、报告 | 是，会覆盖 `reports/run-001-report.md` |

## 推荐学习方式

1. 先阅读对应阶段的 `lessons/<stage>/README.md`。
2. 再阅读实现目录中的 README。
3. 运行 demo，观察输入、输出和中间日志。
4. 对照 `solutions/<stage>/` 中的答案讲解，理解为什么这样设计。
5. 修改一个小点，例如增加样例数据、工具、评分规则或停止条件，再运行测试。

## 本地验证

```bash
make check
make demo-tool
make demo-rag QUERY="RAG 为什么需要引用"
make demo-agent
make demo-eval
```

说明：`make check` 只做编译和单元测试，不运行会覆盖报告文件的 demo。
