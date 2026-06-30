# Labs 常见问题排查

本文整理学习 labs 时常见的问题和排查方法。排障时建议先读错误信息，再从最小命令开始验证。

## 1. 找不到命令

现象：

```text
command not found: node
command not found: python
command not found: git
```

排查：

1. 确认工具是否安装。
2. 确认终端是否重新打开。
3. 确认 PATH 是否包含工具路径。

可运行：

```bash
which node
which python
which python3
which git
```

如果 `python` 不存在但 `python3` 存在，课程命令中的 `python` 可以替换为 `python3`。

## 2. npm install 失败

常见原因：

- Node.js 版本过低。
- 网络不稳定。
- package-lock 与当前环境不兼容。
- 项目本身没有 `package.json`。

排查步骤：

```bash
node --version
npm --version
ls
```

先确认当前目录是否真的有 `package.json`。如果没有，不要继续运行 `npm install`，先回到 lab README 查看推荐目录。

## 3. Python 包导入失败

现象：

```text
ModuleNotFoundError: No module named 'xxx'
```

排查：

1. 是否激活虚拟环境。
2. 是否安装依赖。
3. 是否使用了正确 Python 版本。

常用命令：

```bash
python --version
python -m pip --version
python -m pip install <package-name>
```

如果课程没有要求某个包，优先用标准库完成练习，不要为了“看起来专业”安装大量依赖。

## 4. API Key 未设置

现象：

```text
Missing API key
ANTHROPIC_API_KEY is not set
```

排查：

```bash
printenv ANTHROPIC_API_KEY
```

如果没有输出，说明当前终端没有设置环境变量。

设置方式：

```bash
export ANTHROPIC_API_KEY="你的真实密钥"
```

注意：不要把真实密钥写进课程仓库。示例文件只写变量名或占位符。

## 5. 模型调用超时或限流

常见原因：

- 网络不稳定。
- 请求太大。
- 并发过高。
- 账号限额不足。
- 服务商临时故障。

解决建议：

- 先用 mock 模式跑通流程。
- 减少输入 token。
- 降低并发。
- 加入重试和超时设置。
- 在日志中记录 `error_type`，不要记录真实 key。

## 6. Eval 分数波动大

常见原因：

- 测试集太少。
- 评分标准不清楚。
- 模型输出随机性较高。
- Judge prompt 不稳定。
- 不同类别样例混在一起只看平均分。

改进建议：

- 增加 golden dataset 数量。
- 固定评分 rubric。
- 按 category 分开统计。
- 高风险样例单独看。
- 关键版本做人工抽检。

## 7. 评测报告只有数字，不知道怎么改

改进报告结构：

- 增加失败用例表格。
- 增加失败原因分类。
- 增加安全问题列表。
- 增加 prompt 或数据集修改建议。
- 增加下一次回归测试范围。

报告的目标不是展示漂亮指标，而是指导下一轮工程改进。

## 8. Claude Code 改了不该改的文件

常见原因：

- `CLAUDE.md` 没有写清项目边界。
- 用户任务描述范围太大。
- slash command 没有要求先计划再执行。
- 没有在修改后检查 diff。

改进建议：

- 在 `CLAUDE.md` 中写明“只修改与任务相关文件”。
- 要求 Agent 先输出计划并等待确认。
- 任务完成后查看修改文件列表。
- 高风险操作必须人工确认。

## 9. Hook 运行后卡住或失败

排查方向：

- hook 命令是否存在。
- 当前目录是否正确。
- 命令是否需要交互输入。
- 命令是否耗时过长。
- 失败后是否有清晰提示。

教学阶段建议 hook 只做轻量检查，例如格式化检查、lint、单元测试子集。不要在 hook 中执行部署、删除、推送等高风险操作。

## 10. 日志文件太大

常见原因：

- 保存了完整输入和完整输出。
- 保存了过多 debug 信息。
- 批量评测没有分 run 管理。

改进建议：

- 日志只保存必要元数据。
- 大文本输出放到 runs，日志只记录路径或摘要。
- 每次评测使用独立 run id。
- 定期清理本地临时文件。

## 通用排障流程

遇到问题时按下面顺序处理：

1. 复制完整错误信息，但注意去掉密钥和隐私。
2. 确认当前目录是否正确。
3. 确认依赖是否安装。
4. 用最小输入复现问题。
5. 查看 README 或检查清单。
6. 如果仍无法解决，记录：环境、命令、错误、已尝试方法。

## 提问模板

当你向老师、同学或 AI 工具求助时，可以使用：

```text
我在完成哪个 lab：
我执行的命令：
期望结果：
实际错误：
我已经尝试：
是否包含真实密钥或隐私：否
```

不要在提问中粘贴真实 API Key、cookie、token 或生产数据。
