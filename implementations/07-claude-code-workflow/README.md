# 07 Claude Code Workflow Demo

这是一个 Claude Code / CLI Agent 工作流模拟 Demo。它不调用 Claude Code，不修改真实文件，只用离线规则演示计划、权限、hook 和总结流程。

## 你会看到什么

- bugfix、feature、review、docs 四类工作流。
- 每个工作流的步骤、建议命令和期望输出。
- 命令权限分类：只读、测试、写入、危险、需要确认。
- hook 示例：编辑后运行编译检查。
- skill 提示：根据任务类型建议使用的工作方式。

## 运行方式

```bash
python implementations/07-claude-code-workflow/main.py --scenario bugfix --show-policy
python implementations/07-claude-code-workflow/main.py --scenario review --show-hooks
```

也可以使用 Makefile：

```bash
make demo-claude-code
```

## 学习重点

- CLI Agent 应先探索和计划，再修改和验证。
- 读文件和运行测试通常低风险；删除、force push、生产操作必须阻止或确认。
- Hook 适合自动执行快速、确定、低风险的检查。

## 运行测试

```bash
python -m unittest tests/test_claude_code_workflow.py
```
