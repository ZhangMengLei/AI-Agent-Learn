# Solutions 答案与讲解

本目录用于在完成练习后查看参考答案、解题思路和常见错误。建议先独立完成 `lessons/` 中的练习，再使用 `checkpoints/` 自查，最后回到这里对照答案。

## 使用原则

1. 先做题，再看答案。
2. 先用 `checkpoints/` 判断自己是否理解，再看这里的讲解。
3. 参考答案不是唯一正确答案，重点看背后的设计理由。
4. 如果你的实现更简单、更安全、更容易测试，可以保留自己的方案。
5. 不要把真实 API Key、cookie、token 或生产数据写进答案和实验记录。

## 答案索引

| 阶段 | 主题 | 练习答案 | 练习 Lab | 项目讲解 | 项目 Lab | 可运行实现 |
| --- | --- | --- | --- | --- | --- | --- |
| 00-ai-foundation | AI 基础导学 | [练习](./00-ai-foundation/03-exercises.md) | [Lab](./00-ai-foundation/04-exercises-lab.md) | [项目](./00-ai-foundation/05-project.md) | [项目 Lab](./00-ai-foundation/06-project-lab.md) | 无，先按课程设计实现 |
| 01-prompt | Prompt Engineering | [练习](./01-prompt/03-exercises.md) | [Lab](./01-prompt/04-exercises-lab.md) | [项目](./01-prompt/05-project.md) | [项目 Lab](./01-prompt/06-project-lab.md) | 无，先按课程设计实现 |
| 02-llm-api | LLM API 与 SDK | [练习](./02-llm-api/03-exercises.md) | [Lab](./02-llm-api/04-exercises-lab.md) | [项目](./02-llm-api/05-project.md) | [项目 Lab](./02-llm-api/06-project-lab.md) | 无，先按课程设计实现 |
| 03-tool-use | Tool Use / Function Calling | [练习](./03-tool-use/03-exercises.md) | [Lab](./03-tool-use/04-exercises-lab.md) | [项目](./03-tool-use/05-project.md) | [项目 Lab](./03-tool-use/06-project-lab.md) | [implementations/03-tool-assistant/](../implementations/03-tool-assistant/) |
| 04-rag | RAG 知识库问答 | [练习](./04-rag/03-exercises.md) | [Lab](./04-rag/04-exercises-lab.md) | [项目](./04-rag/05-project.md) | [项目 Lab](./04-rag/06-project-lab.md) | [implementations/04-rag-assistant/](../implementations/04-rag-assistant/) |
| 05-agent | Agent 架构 | [练习](./05-agent/03-exercises.md) | [Lab](./05-agent/04-exercises-lab.md) | [项目](./05-agent/05-project.md) | [项目 Lab](./05-agent/06-project-lab.md) | [implementations/05-research-agent/](../implementations/05-research-agent/) |
| 06-mcp | MCP | [练习](./06-mcp/03-exercises.md) | [Lab](./06-mcp/04-exercises-lab.md) | [项目](./06-mcp/05-project.md) | [项目 Lab](./06-mcp/06-project-lab.md) | 无，先按课程设计实现 |
| 07-claude-code | Claude Code / CLI Agent | [练习](./07-claude-code/03-exercises.md) | [Lab](./07-claude-code/04-exercises-lab.md) | [项目](./07-claude-code/05-project.md) | [项目 Lab](./07-claude-code/06-project-lab.md) | 无，先按课程设计实现 |
| 08-eval-security | Eval / Security | [练习](./08-eval-security/03-exercises.md) | [Lab](./08-eval-security/04-exercises-lab.md) | [项目](./08-eval-security/05-project.md) | [项目 Lab](./08-eval-security/06-project-lab.md) | [implementations/08-eval-lab/](../implementations/08-eval-lab/) |

## 答案格式约定

每个练习答案尽量包含：

```text
参考答案：给出可直接对照的答案或示例。
为什么这样答：解释关键概念和设计取舍。
常见错误：指出初学者容易犯的错误。
可选扩展：给已经完成基础要求的学习者继续深入的方向。
```

项目类答案更关注设计与验收：

- 推荐架构
- 核心模块
- 运行与测试方式
- 验收标准
- 常见风险
- 可选扩展

## 学习建议

如果你刚开始学习，建议按下面顺序使用：

1. 阅读 `lessons/<stage>/01-basic.md` 和 `02-templates.md`。
2. 完成 `lessons/<stage>/03-exercises.md`。
3. 对照 `solutions/<stage>/03-exercises.md`。
4. 进入 `04-exercises-lab` 和 `06-project-lab` 做工程练习。
5. 使用对应 solutions 文件复盘实现质量。
