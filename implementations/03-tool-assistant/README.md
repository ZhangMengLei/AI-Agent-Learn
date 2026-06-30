# Tool Use 可运行教学 Demo

这是一个面向初学者的 Tool Use / Function Calling 最小实现。它不调用真实 LLM API，也不需要 API Key，而是用一个规则型 `MockModel` 模拟“模型根据用户输入选择工具”的过程。

## 目标

通过一个可运行的命令行小助手理解 Tool Use 的核心链路：

1. 用户输入自然语言。
2. Mock 模型把输入转换为结构化 `ToolCall`。
3. `ToolRegistry` 查找工具并校验参数。
4. 根据工具权限决定是否需要确认。
5. 执行工具并记录 tool log。
6. 把工具结果组织成最终回复。

## 运行方式

在仓库根目录执行：

```bash
python implementations/03-tool-assistant/main.py "北京天气怎么样"
python implementations/03-tool-assistant/main.py "计算 1 + 2 * 3"
python implementations/03-tool-assistant/main.py --yes "记录 今天学习 Tool Use"
```

不传入消息时进入交互模式：

```bash
python implementations/03-tool-assistant/main.py
```

交互模式示例：

```text
> 北京天气怎么样
> 计算 8 / 2 + 3
> 记录 今天理解了 tool registry
> 查看笔记
> exit
```

说明：`mock_notes` 是写入类工具，默认会询问确认；命令行加入 `--yes` 可以自动允许。

## 目录结构

```text
implementations/03-tool-assistant/
  README.md        本说明文档
  main.py          Demo 全部实现，便于初学者阅读

tests/
  test_tool_assistant.py
```

## 已实现工具

- `calculator`：安全计算四则表达式和少量数学运算，不使用 `eval`。
- `mock_weather`：返回固定的模拟天气数据，不访问网络。
- `mock_notes`：内存笔记写入工具，用来演示写权限确认。
- `list_notes`：读取内存笔记。

## 学习点

- Tool registry：工具注册、元数据、统一执行入口。
- 参数校验：执行前检查必填参数、参数类型和未知参数。
- 权限等级：`public`、`read`、`write` 三类权限；写权限需要确认。
- Tool log：每次工具调用都会记录工具名、参数、权限、状态和时间。
- Mock model：用规则模拟 LLM 的工具选择，帮助先理解工程骨架。
- 安全计算器：用 AST 白名单替代危险的 `eval`。

## 如何扩展到真实 LLM

真实 LLM 接入点在 `main.py` 的 `MockModel.plan()`：

- 当前：用关键词和正则把用户输入映射成 `ToolCall(name, arguments)`。
- 真实 LLM：把工具列表转成模型支持的 tools / functions schema，让模型返回工具名和 JSON 参数。
- 保持不变：`ToolRegistry.execute()`、参数校验、权限确认、tool log 都可以继续复用。

替换时建议保留这条边界：

```text
LLM 输出结构化 ToolCall -> ToolRegistry 执行 -> ToolResult -> 最终回复
```

这样即使模型提供商变化，工具执行层仍然稳定。

## 运行测试

```bash
python -m unittest discover -s tests
```
