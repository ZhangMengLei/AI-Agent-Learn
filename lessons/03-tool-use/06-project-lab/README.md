# Tool Use 项目实现工程说明

本项目实验要求你实现一个可运行的“工具调用助手”。它能够接收用户输入，判断是否需要调用工具，生成工具参数，执行工具，并基于工具结果给出最终回答。

项目重点是工程链路，而不是工具数量。请优先保证每一步可观察、可调试、可回退。

## 项目目标

实现一个命令行版 Tool Use Assistant，具备以下能力：

1. 支持普通问答和工具问答两类请求。
2. 支持计算器、Mock 天气、Mock 笔记读取三个低/中风险工具。
3. 支持一个高风险模拟工具，并在执行前进行人工确认。
4. 对工具参数做校验，对工具错误做友好提示。
5. 保存工具调用日志，方便复盘模型是否选对工具。

## 推荐文件结构

可以在本目录下按下面结构实现：

```text
04-project-lab/
  README.md
  pyproject.toml 或 package.json
  src/
    app.py                    # 程序入口
    config.py                 # 配置读取，不保存真实 API Key
    llm_client.py             # 大模型调用封装，可先用 mock
    conversation.py           # 对话主流程
    tool_registry.py          # 工具注册表
    permission_guard.py       # 权限确认
    logger.py                 # 调用日志
    tools/
      __init__.py
      calculator.py
      weather.py
      notes.py
      dangerous_actions.py
    data/
      weather.json
      notes.json
    prompts/
      system_prompt.txt
      tool_result_prompt.txt
  tests/
    test_tool_registry.py
    test_permission_guard.py
    test_calculator.py
```

不要求完全照抄，但建议保留三个核心模块：

- `tool_registry`：统一管理工具名称、Schema、风险等级、执行函数。
- `permission_guard`：统一判断工具是否需要确认。
- `conversation`：串起用户输入、模型调用、工具执行和最终回答。

## 最小可运行流程

```text
用户输入
  ↓
构造消息和工具 Schema
  ↓
调用模型或 mock 决策器
  ↓
如果模型返回工具调用：
  1. 校验工具名是否存在
  2. 校验参数是否符合 Schema
  3. 判断风险等级
  4. 必要时请求用户确认
  5. 执行工具
  6. 把工具结果回传模型或模板化生成答案
  ↓
输出最终回答
```

## 实现步骤

### 第 1 步：定义工具注册表

每个工具至少包含：

- `name`：工具名。
- `description`：什么时候使用。
- `parameters`：JSON Schema 或等价结构。
- `risk_level`：`low`、`medium`、`high`。
- `handler`：实际执行函数。

示例工具：

```text
calculate(expression)       low     数学计算
get_weather(city)           low     查询 Mock 天气
read_note(title)            medium  读取预设学习笔记
delete_note(title)          high    模拟删除笔记，必须确认
```

### 第 2 步：实现工具函数

要求：

- 函数只接收结构化参数。
- 返回统一格式，例如：

```json
{
  "ok": true,
  "data": {},
  "error": null
}
```

失败时：

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "CITY_NOT_FOUND",
    "message": "暂未找到该城市的 Mock 天气数据"
  }
}
```

### 第 3 步：接入模型或 Mock 决策器

初学阶段可以先使用 Mock 决策器：

- “天气” → `get_weather`
- “计算”或数学表达式 → `calculate`
- “笔记” → `read_note`
- “删除” → `delete_note`

进阶阶段再替换为真实大模型 Tool Use。注意不要在代码中写真实 API Key，应通过环境变量读取。

### 第 4 步：加入权限确认

推荐策略：

| 风险等级 | 示例 | 处理方式 |
| --- | --- | --- |
| low | 计算、天气 | 自动执行 |
| medium | 读取预设笔记 | 记录日志后执行 |
| high | 删除、发送、修改、执行命令 | 展示参数并要求确认 |

确认提示建议包含：

- 将要执行的工具名。
- 将要使用的参数。
- 可能影响。
- 如何取消。

### 第 5 步：加入日志和调试输出

每次工具调用建议记录：

- 时间。
- 用户输入。
- 模型选择的工具名。
- 参数。
- 风险等级。
- 是否经过确认。
- 工具执行结果。

日志可以先写到控制台，进阶后写到本地 JSONL 文件。

## 验收方式

使用下面场景逐项验证：

1. 普通问答：`什么是 Function Calling？` 不应强制调用工具。
2. 计算：`帮我计算 99 * 18` 应调用 `calculate` 并返回正确结果。
3. 天气：`上海天气怎么样？` 应调用 `get_weather`。
4. 笔记：`读取 tool-use-basics 笔记` 应调用 `read_note`。
5. 高风险：`删除 tool-use-basics 笔记` 必须先确认，默认取消不执行。
6. 错误参数：`查询火星天气` 应给出可理解的失败原因。
7. 日志检查：能追踪工具选择、参数和执行结果。

## 常见扩展

- 增加工具重试和超时控制。
- 增加工具结果摘要，避免把过长结果直接塞回模型。
- 增加工具调用评测集，统计模型选工具准确率。
- 把命令行改造成 Web UI。
- 将 RAG 检索作为一个新工具接入。
