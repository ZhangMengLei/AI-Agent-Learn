from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class WorkflowStep:
    name: str
    description: str
    allowed_commands: List[str]
    expected_output: str


class CommandPolicy:
    destructive_markers = ["rm -rf", "git reset --hard", "git push --force", "drop database", "delete production"]
    write_markers = ["git commit", "git push", "edit", "write", "touch", "mkdir", "apply patch"]
    test_markers = ["unittest", "pytest", "make test", "make check", "compileall"]
    read_markers = ["ls", "find", "grep", "read", "git status", "git diff", "git log"]

    def classify(self, command: str) -> str:
        lowered = command.lower()
        if any(marker in lowered for marker in self.destructive_markers):
            return "destructive"
        if any(marker in lowered for marker in self.test_markers):
            return "test"
        if any(marker in lowered for marker in self.write_markers):
            return "write"
        if any(lowered.startswith(marker) or marker in lowered for marker in self.read_markers):
            return "read_only"
        return "ask"

    def decision(self, command: str) -> str:
        category = self.classify(command)
        return {"read_only": "allow", "test": "allow", "write": "ask", "destructive": "block", "ask": "ask"}[category]


class ClaudeCodeWorkflowPlanner:
    def plan_for_scenario(self, scenario: str) -> List[WorkflowStep]:
        if scenario == "review":
            return [
                WorkflowStep("读取变更", "查看 git diff 和相关文件。", ["git status", "git diff"], "理解改动范围"),
                WorkflowStep("风险审查", "检查安全、测试和边界影响。", ["grep", "read"], "列出风险和问题"),
                WorkflowStep("测试建议", "给出应运行的测试和缺口。", ["make check"], "测试计划"),
                WorkflowStep("总结", "输出可执行 review 结论。", [], "通过/需修改/阻塞"),
            ]
        if scenario == "docs":
            return [
                WorkflowStep("读取文档结构", "查看 README 和课程目录。", ["find", "read"], "定位应修改文档"),
                WorkflowStep("制定计划", "说明新增内容和链接位置。", [], "文档计划"),
                WorkflowStep("更新文档", "按计划编辑文档。", ["edit"], "文档变更"),
                WorkflowStep("验证链接", "检查本地链接和目录。", ["make check"], "验证结果"),
            ]
        if scenario == "feature":
            return [
                WorkflowStep("探索代码", "读取相关模块和测试。", ["find", "grep", "read"], "找到修改点"),
                WorkflowStep("计划实现", "先写清楚方案和风险。", [], "实施计划"),
                WorkflowStep("实现功能", "修改代码和测试。", ["edit", "write"], "功能变更"),
                WorkflowStep("运行验证", "运行编译和测试。", ["make check"], "测试通过"),
                WorkflowStep("总结", "说明改了什么和如何验证。", [], "交付摘要"),
            ]
        return [
            WorkflowStep("探索", "读取项目说明、相关代码和测试。", ["git status", "find", "grep", "read"], "定位问题范围"),
            WorkflowStep("计划", "说明根因、修改点和验证方式。", [], "用户可审阅的计划"),
            WorkflowStep("实现", "最小范围修复代码并补充测试。", ["edit", "write"], "代码变更"),
            WorkflowStep("测试", "运行相关测试和全量检查。", ["make check"], "验证通过"),
            WorkflowStep("总结", "简要说明变更和后续风险。", [], "完成说明"),
        ]


class HookExampleBuilder:
    def build(self) -> Dict[str, object]:
        return {
            "name": "compile-after-edit",
            "trigger": "After editing Python files",
            "command": "python3 -m compileall -q implementations tests",
            "on_failure": "Stop and fix syntax errors before summarizing work.",
        }


class SkillHintRouter:
    def suggest(self, task: str) -> List[str]:
        lowered = task.lower()
        hints = []
        if "review" in lowered or "审查" in task:
            hints.append("code review checklist")
        if "security" in lowered or "安全" in task:
            hints.append("security review")
        if "test" in lowered or "测试" in task:
            hints.append("test planning")
        if not hints:
            hints.append("general implementation workflow")
        return hints


def render_plan(scenario: str, show_policy: bool, show_hooks: bool) -> str:
    planner = ClaudeCodeWorkflowPlanner()
    policy = CommandPolicy()
    lines = [f"场景：{scenario}", "", "工作流步骤："]
    for index, step in enumerate(planner.plan_for_scenario(scenario), 1):
        commands = ", ".join(step.allowed_commands) if step.allowed_commands else "无命令，先输出说明"
        lines.append(f"{index}. {step.name}：{step.description}")
        lines.append(f"   建议命令：{commands}")
        lines.append(f"   期望输出：{step.expected_output}")
    if show_policy:
        samples = ["git status", "make check", "edit README.md", "git push --force", "rm -rf data"]
        lines.extend(["", "权限策略示例："])
        for command in samples:
            lines.append(f"- {command}: {policy.classify(command)} -> {policy.decision(command)}")
    if show_hooks:
        lines.extend(["", "Hook 示例：", str(HookExampleBuilder().build())])
    lines.extend(["", "Skill 提示：" + ", ".join(SkillHintRouter().suggest(scenario))])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Claude Code 工作流模拟教学 Demo")
    parser.add_argument("--scenario", choices=["bugfix", "feature", "review", "docs"], default="bugfix")
    parser.add_argument("--show-policy", action="store_true")
    parser.add_argument("--show-hooks", action="store_true")
    args = parser.parse_args()
    print(render_plan(args.scenario, args.show_policy, args.show_hooks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
