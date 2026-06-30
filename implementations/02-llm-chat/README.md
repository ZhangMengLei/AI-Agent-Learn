# 02 Mock LLM Chat

这是一个离线版 LLM API 教学 Demo，只使用 Python 标准库，不访问网络，不读取真实 API Key。

## 你会看到什么

- `messages` 结构：system、user、assistant。
- mock completion：模拟一次完整响应。
- mock streaming：把响应拆成 chunk 输出。
- 多轮上下文：保留 system message 和最近历史。
- 调用日志：model、token 估算、latency、temperature、max_tokens。

## 运行方式

```bash
python implementations/02-llm-chat/main.py "解释 temperature 是什么" --show-log
python implementations/02-llm-chat/main.py "什么是 streaming" --stream
python implementations/02-llm-chat/main.py --multi-turn --show-log
```

也可以使用 Makefile：

```bash
make demo-llm
```

## 学习重点

- LLM API 通常是无状态的，多轮对话需要应用自己传入必要历史。
- Streaming 改善体验，但不一定降低总 token 成本。
- 日志应记录排障和成本指标，但不能记录真实密钥或敏感原文。

## 如何扩展到真实 SDK

保留 `Conversation`、`CallLogger` 和日志结构，把 `MockLLMClient` 替换为真实 SDK 调用即可。真实 API Key 必须从环境变量或本地 `.env` 读取，不能写入仓库。

## 运行测试

```bash
python -m unittest tests/test_llm_chat.py
```
