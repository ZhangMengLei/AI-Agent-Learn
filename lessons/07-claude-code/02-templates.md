# Claude Code 常用模板

## CLAUDE.md 模板

```markdown
# Project Guide

## 项目简介

这里说明项目做什么。

## 常用命令

- 安装依赖：`npm install`
- 启动开发：`npm run dev`
- 运行测试：`npm test`
- 类型检查：`npm run typecheck`

## 代码规范

- 保持函数职责单一
- 优先修改现有文件
- 不要引入不必要抽象

## 注意事项

- 不要提交真实密钥
- 高风险 Git 操作需要用户确认
- UI 修改需要实际打开页面验证
```

## Slash Command 模板

```markdown
# /summarize-pr

请总结当前分支相对 main 的变更。

步骤：
1. 查看 git status
2. 查看提交历史
3. 查看 diff
4. 输出 Summary 和 Test Plan
```

## Hook 配置思路

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run format"
          }
        ]
      }
    ]
  }
}
```

## 权限策略模板

```text
允许：
- 读取文件
- 搜索代码
- 运行测试

需要确认：
- 安装依赖
- 删除文件
- git push
- 修改 CI/CD

禁止自动执行：
- reset --hard
- push --force
- 删除数据库
```

## 自动化工作流模板

```text
需求输入
  ↓
阅读相关代码
  ↓
制定计划
  ↓
用户确认
  ↓
修改代码
  ↓
运行测试
  ↓
总结变更
```

## Code Review 输出模板

```markdown
## Summary

- 本次变更做了什么

## Risks

- 可能的风险点

## Suggestions

- 建议修改项

## Test Plan

- 已执行或建议执行的测试
```
