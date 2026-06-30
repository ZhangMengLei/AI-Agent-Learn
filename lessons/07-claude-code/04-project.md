# Claude Code 实战项目：自动化工作流

## 项目目标

设计一套 Claude Code 工作流，用来处理一个常见软件工程任务：阅读需求、修改代码、运行测试、总结变更。

## 工作流场景

示例任务：

```text
为项目添加一个表单校验功能，并补充测试。
```

## 流程设计

```text
接收需求
  ↓
搜索相关代码
  ↓
阅读关键文件
  ↓
制定实现计划
  ↓
用户确认
  ↓
修改代码
  ↓
运行测试
  ↓
修复问题
  ↓
输出总结
```

## 推荐项目文件

```text
claude-workflow/
  README.md
  CLAUDE.md
  commands/
    implement-feature.md
    review-change.md
    summarize-work.md
  hooks/
    format-after-edit.json
  examples/
```

## 必备内容

### 1. CLAUDE.md

说明项目规则、测试命令、注意事项。

### 2. Slash Command

设计一个 `/implement-feature` 工作流。

### 3. Hook

设计一个编辑后格式化或测试前检查 hook。

### 4. 权限策略

说明哪些操作允许自动执行，哪些必须确认。

## 验收标准

- 有清晰 CLAUDE.md。
- 有至少一个 slash command 设计。
- 有至少一个 hook 设计。
- 有权限策略说明。
- 能说明完整工作流如何运行。

## 扩展方向

- 接入 MCP Server。
- 增加代码审查工作流。
- 增加安全审查工作流。
- 增加 PR 自动总结工作流。
