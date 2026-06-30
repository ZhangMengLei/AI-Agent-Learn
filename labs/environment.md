# 学习工程环境指南

本文说明完成课程 labs 推荐准备的本地环境。你不需要一次安装所有工具，可以按阶段逐步补齐。

## 基础环境

建议准备：

- 操作系统：macOS、Linux 或 Windows + WSL。
- Git：用于查看 diff、管理代码版本。
- Node.js：适合前端、CLI、MCP 示例。
- Python：适合 RAG、Eval、脚本统计示例。
- VS Code 或其他编辑器。
- Claude Code 或你正在使用的 AI 编程助手。

推荐版本：

```text
Git >= 2.40
Node.js >= 20
Python >= 3.10
```

版本不是绝对要求。初学阶段更重要的是能稳定运行命令、阅读报错并逐步排查。

## 检查命令

可以用下面命令确认环境：

```bash
git --version
node --version
npm --version
python --version
```

如果你的系统中 Python 命令是 `python3`，可以使用：

```bash
python3 --version
```

## 推荐工作流

每次进入一个 lab，建议按下面步骤：

1. 阅读该目录的 `README.md`。
2. 查看推荐文件结构。
3. 先创建最小文件，不要一开始追求完整。
4. 用 mock 数据或示例输入跑通流程。
5. 再逐步替换为真实实现。
6. 最后用检查清单验收。

## Python 项目建议

Eval、安全、RAG 类实验适合使用 Python。

推荐做法：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows PowerShell 可使用：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

如果课程没有提供 `requirements.txt`，不要盲目安装大量依赖。先用标准库实现最小版本。

## Node.js 项目建议

Claude Code、CLI、MCP 类实验可能使用 Node.js。

推荐做法：

```bash
npm install
npm test
npm run lint
```

如果某个命令不存在，先查看 `package.json` 中的 `scripts` 字段，不要猜测命令。

## 文件和目录安全

学习实验中请避免：

- 在仓库中创建 `.env` 并写入真实密钥。
- 把真实生产数据复制进 `datasets/`。
- 把大体积日志、模型输出、缓存目录提交到仓库。
- 执行不理解的删除、覆盖、推送命令。

建议：

- 使用 `.env.example` 展示变量名，不展示真实值。
- 使用 mock 数据或脱敏数据。
- 在运行脚本前先读脚本说明。
- 改动后查看 diff。

## Claude Code 学习环境建议

在 07 阶段，重点不是记住所有配置细节，而是理解工程边界：

- `CLAUDE.md`：告诉 Agent 项目规则。
- slash command：把重复流程沉淀为命令。
- hooks：在关键节点自动检查。
- settings：配置权限和环境变量。

建议先在小项目中试验，不要直接在重要仓库中开放高权限自动化。

## Eval 学习环境建议

在 08 阶段，建议先用本地 mock 流程：

1. 手写 `golden.jsonl`。
2. 用 mock answer 生成 `run-001.jsonl`。
3. 人工评分。
4. 生成报告。

等数据结构和报告逻辑稳定后，再接入真实模型 API。
