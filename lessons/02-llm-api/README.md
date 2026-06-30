# 02 LLM API 与 SDK

## 学习目标

从使用 AI 产品进入开发 AI 应用，掌握模型 API 的基本调用方式。

## 学习内容

- [基础讲解](01-basic.md)
- [常用模板](02-templates.md)
- [练习任务](03-exercises.md)
- [练习工程](04-exercises-lab/README.md)
- [实战项目](05-project.md)
- [项目工程](06-project-lab/README.md)
- [阶段复盘](07-review.md)

## 核心概念

- API Key
- Model
- Messages
- Temperature
- Max Tokens
- Streaming
- Token 计费
- Rate Limit
- Prompt Caching
- 多轮对话上下文
- Mock Provider 与 Real Provider
- Provider / Model / Env 配置分层
- 安全切换与回滚
- 超时、重试、限流和错误分类

## 学习任务

1. 完成一次最小 API 调用。
2. 实现多轮对话。
3. 实现流式输出。
4. 记录调用日志。
5. 理解 token、延迟和成本。
6. 将 mock 调用封装成 provider 接口，为真实 API 替换做准备。
7. 使用环境变量区分 dev / test / prod，不在代码或文档中写真实密钥。
8. 为真实 API 调用设计超时、重试、错误分类和降级回 mock 的策略。

## 真实 API 替换路线

教学工程建议先跑通 mock，再替换为真实 API。不要让业务代码直接依赖某个 SDK，而是抽象出统一接口：

```text
ChatProvider.generate(messages, options) -> 完整回答
ChatProvider.stream(messages, options) -> 文本片段迭代器
```

推荐配置分层：

| 配置项 | 示例 | 说明 |
| --- | --- | --- |
| `LLM_PROVIDER` | `mock` / `anthropic` / `openai-compatible` | 控制当前使用的 provider |
| `LLM_API_KEY_ENV` | `ANTHROPIC_API_KEY` | 只保存环境变量名，不保存真实值 |
| `LLM_MODEL` | `model-name` | 模型名从配置读取，便于切换 |
| `LLM_BASE_URL` | `https://api.example.com` | 仅在需要兼容接口时配置 |
| `LLM_TIMEOUT_MS` | `30000` | 防止请求长时间挂起 |
| `LLM_MAX_RETRIES` | `2` | 只对临时错误重试 |

切换步骤：

1. mock provider 先通过多轮、streaming、日志和错误处理测试。
2. 本机设置真实 API Key 环境变量，但不写入仓库。
3. 将 `LLM_PROVIDER` 从 `mock` 改为真实 provider。
4. 用低成本模型和小输入完成 smoke test。
5. 确认日志脱敏、错误分类、超时和限流处理正常。
6. 出现鉴权、限流或成本异常时，立即切回 `mock` 或禁用真实调用。

## 实战项目

做一个命令行 AI 聊天助手。
