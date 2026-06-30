import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "implementations" / "07-claude-code-workflow" / "main.py"
SPEC = importlib.util.spec_from_file_location("claude_code_workflow", MODULE_PATH)
workflow = importlib.util.module_from_spec(SPEC)
sys.modules["claude_code_workflow"] = workflow
assert SPEC.loader is not None
SPEC.loader.exec_module(workflow)


class ClaudeCodeWorkflowTest(unittest.TestCase):
    def test_command_policy_classifies_commands(self):
        policy = workflow.CommandPolicy()
        self.assertEqual("read_only", policy.classify("git status"))
        self.assertEqual("test", policy.classify("make check"))
        self.assertEqual("write", policy.classify("git commit"))
        self.assertEqual("destructive", policy.classify("git push --force"))

    def test_bugfix_plan_contains_core_steps(self):
        steps = workflow.ClaudeCodeWorkflowPlanner().plan_for_scenario("bugfix")
        names = [step.name for step in steps]
        self.assertEqual(["探索", "计划", "实现", "测试", "总结"], names)

    def test_review_plan_contains_risk_step(self):
        steps = workflow.ClaudeCodeWorkflowPlanner().plan_for_scenario("review")
        self.assertIn("风险审查", [step.name for step in steps])

    def test_hook_example_contains_no_secret(self):
        hook = workflow.HookExampleBuilder().build()
        text = str(hook).lower()
        self.assertIn("command", hook)
        self.assertNotIn("api_key", text)
        self.assertNotIn("token", text)

    def test_render_plan_is_stable(self):
        text = workflow.render_plan("bugfix", show_policy=True, show_hooks=False)
        self.assertIn("权限策略示例", text)
        self.assertIn("git push --force: destructive -> block", text)


if __name__ == "__main__":
    unittest.main()
