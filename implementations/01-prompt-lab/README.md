# 01 Prompt Lab

这是一个面向初学者的 Prompt Engineering 可运行 Demo，只使用 Python 标准库，不调用真实模型。

## 你会看到什么

- Prompt 模板库：总结、代码解释、需求拆解、JSON 抽取。
- 结构化 Prompt 渲染。
- Prompt 质量检查：角色、任务、上下文、约束、输出格式、验收标准。
- 随口 Prompt 与结构化 Prompt 的对比。
- 稳定的 mock 输出，方便课堂演示和测试。

## 运行方式

```bash
python implementations/01-prompt-lab/main.py --template summarize --input "Prompt 是人与大模型协作时的任务说明书。" --compare
python implementations/01-prompt-lab/main.py --template json_extract --input "我叫小李，是后端工程师，想学习 Agent 和 MCP。"
```

也可以使用 Makefile：

```bash
make demo-prompt
```

## 学习重点

- 好 Prompt 不只是问题，而是角色、任务、上下文、约束、输出格式和验收标准的组合。
- 输出格式越明确，越容易被程序解析和测试。
- 对比实验能帮助你判断 Prompt 改动是否真的变好。

## 如何扩展

- 增加新的 `PromptTemplate`。
- 为模板增加更多样例输入。
- 把 `MockPromptRunner` 替换为真实 LLM 调用，但 API Key 必须来自环境变量或本地 `.env`。

## 运行测试

```bash
python -m unittest tests/test_prompt_lab.py
```
