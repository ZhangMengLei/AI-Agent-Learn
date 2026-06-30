# LLM API 基础

## LLM API 是什么

LLM API 是把大模型能力接入自己程序的方式。

你不再只是打开网页和 AI 聊天，而是可以在自己的应用里调用模型，让模型完成生成、总结、分析、问答、工具调用等任务。

## 一次 API 调用通常包含什么

```text
用户输入 → 构造 messages → 调用模型 API → 获取模型输出 → 展示或继续处理
```

## 核心参数

### model

指定使用哪个模型。

不同模型在能力、速度、价格上不同。

### messages

表示对话内容，通常包含：

- system：系统指令
- user：用户输入
- assistant：模型历史回复

### temperature

控制输出随机性。

- 低 temperature：更稳定，适合代码、结构化输出
- 高 temperature：更多样，适合创意写作

### max_tokens

限制最大输出长度。

### stream

是否使用流式输出。

流式输出可以让用户更快看到内容，而不是等模型全部生成完。

## 多轮对话

多轮对话不是模型自动记住所有内容，而是程序每次请求时把必要历史重新传给模型。

需要注意：

- 历史太长会消耗更多 token
- 上下文窗口有限
- 长对话需要摘要或裁剪

## Token 与成本

Token 可以粗略理解为模型处理文本的最小单位。

成本通常由下面几部分决定：

- 输入 token
- 输出 token
- 模型单价
- 是否使用缓存

## Prompt Caching

Prompt Caching 用于缓存重复的大段上下文，减少延迟和成本。

适合场景：

- 固定系统提示词
- 固定工具说明
- 长文档上下文
- 多轮任务中的稳定前缀

## Mock 到真实 API 的安全切换

学习阶段推荐先使用 mock provider。mock 的价值不是“假装调用成功”，而是让你在不消耗费用、不暴露密钥的情况下，先把交互循环、messages 组装、streaming、日志和错误处理跑通。

### Provider 抽象

不要把 SDK 调用散落在业务代码里。建议只让业务层依赖统一接口：

```text
generate(messages, options) -> { text, usage, raw }
stream(messages, options) -> 逐步返回 delta 文本，结束后返回 usage
```

这样后续从 mock 切到真实 API 时，只替换 provider 实现，不需要重写命令行交互、历史管理或日志模块。

### Env 与配置设计

推荐把“环境”“provider”“密钥变量名”分开：

```text
APP_ENV=dev
LLM_PROVIDER=mock
LLM_API_KEY_ENV=ANTHROPIC_API_KEY
LLM_MODEL=model-name
LLM_TIMEOUT_MS=30000
LLM_MAX_RETRIES=2
```

规则：

- `dev` 默认使用 mock，除非学习者显式切换。
- `test` 必须使用 mock 或录制的 fixture，避免 CI 调真实 API。
- `prod` 必须检查 API Key、预算、日志脱敏和限流策略。
- 配置文件只写环境变量名和占位符，不写真实密钥。

### Streaming 处理

真实 streaming 不是一次返回完整文本，而是多个片段陆续到达。实现时要注意：

- 收到 delta 后立即打印，改善体感延迟。
- 同时把 delta 追加到 buffer，请求结束后保存完整 assistant message。
- 如果流中途失败，日志要记录 partial output，并提示用户“回答可能不完整”。
- 不要在每个 delta 都写一次完整历史，避免频繁 IO。

### 错误分类与恢复

至少区分这些错误：

| 错误类型 | 常见原因 | 建议处理 |
| --- | --- | --- |
| `missing_key` | 未设置环境变量 | 给出设置指引，不重试 |
| `auth_error` | Key 无效或权限不足 | 停止调用，提示检查 Key |
| `rate_limit` | 请求过快或额度不足 | 指数退避，达到上限后失败 |
| `timeout` | 网络慢或模型响应慢 | 可重试，记录耗时 |
| `server_error` | 服务商临时异常 | 可重试，必要时降级 |
| `bad_request` | 参数、messages 或模型名错误 | 不重试，提示修正配置 |
| `empty_output` | 返回为空或被截断 | 记录原始状态，提示重试 |

真实 API 替换的最低验收：mock 路径仍可运行；真实路径不会打印或提交 API Key；失败时能给出可理解错误，而不是直接崩溃。

## 常见错误

- API Key 无效
- 请求频率过高
- 参数格式错误
- 输出超出限制
- 网络超时
- 模型名称写错

## 一句话总结

LLM API 的重点不是只会调接口，而是能管理上下文、成本、延迟、输出格式和错误处理。
