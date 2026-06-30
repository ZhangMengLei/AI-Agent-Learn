# API Key 安全指南

AI 工程实验经常需要调用模型 API。API Key 相当于账号密码，必须谨慎处理。本课程所有示例都不应该出现真实 API Key。

## 基本原则

请牢记：

- 不要把真实 API Key 写进代码。
- 不要把真实 API Key 写进 README、Markdown、Notebook 输出或截图。
- 不要把真实 API Key 提交到 git。
- 不要在日志中打印 API Key。
- 不要把 API Key 发给不可信工具或网页。
- 如果怀疑泄露，立即去服务商控制台撤销并重新生成。

## 推荐方式：环境变量

使用环境变量保存密钥：

```bash
export ANTHROPIC_API_KEY="你的真实密钥只放在本机环境变量中"
```

代码中只读取变量名：

```python
import os

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("请先设置 ANTHROPIC_API_KEY 环境变量")
```

不要写成：

```python
api_key = "sk-真实密钥"
```

## .env 文件注意事项

如果你使用 `.env`：

- `.env` 只能保存在本机，不应提交到仓库。
- 仓库中可以放 `.env.example`，只展示变量名。
- `.env.example` 中不要写真实值。

示例 `.env.example`：

```text
ANTHROPIC_API_KEY=replace_with_your_key
MODEL_NAME=replace_with_model_name
```

## 在教学材料中如何写

推荐写法：

```text
请设置环境变量 ANTHROPIC_API_KEY。
```

或：

```json
{
  "api_key_env": "ANTHROPIC_API_KEY"
}
```

不推荐写法：

```json
{
  "api_key": "sk-xxxx"
}
```

## 日志脱敏

错误示例：

```text
request failed, api_key=sk-xxxx, input=用户完整隐私数据
```

推荐示例：

```json
{
  "request_id": "req-001",
  "success": false,
  "error_type": "rate_limit",
  "api_key_suffix": "****1234",
  "input_preview": "已脱敏的前 20 个字符"
}
```

更好的方式是完全不记录 key，只记录错误类型和 request id。

## 权限最小化

如果服务商支持，请为学习实验创建单独的 key：

- 设置预算上限。
- 设置可访问模型范围。
- 避免使用生产项目 key。
- 定期轮换。
- 课程结束后删除不用的 key。

## 常见泄露场景

- 把 `.env` 误提交到 git。
- 在 Notebook 输出中打印环境变量。
- 在报错截图中暴露请求头。
- 在 debug 日志中打印完整 HTTP 请求。
- 把包含 key 的配置发给 AI 工具分析。

## 发现泄露怎么办

1. 立即撤销泄露的 API Key。
2. 重新生成新的 API Key。
3. 检查账单和调用记录。
4. 从 git 历史、日志、截图、文档中清理泄露内容。
5. 复盘泄露原因，补充 `.gitignore` 和检查流程。

## Lab 检查清单

- [ ] 代码中没有真实 API Key。
- [ ] Markdown 中没有真实 API Key。
- [ ] 日志中没有真实 API Key。
- [ ] 示例配置使用 `*_ENV` 或占位符。
- [ ] 使用 mock 数据时没有混入生产数据。
- [ ] 高风险操作需要人工确认。
