import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "implementations" / "01-prompt-lab" / "main.py"
SPEC = importlib.util.spec_from_file_location("prompt_lab", MODULE_PATH)
prompt_lab = importlib.util.module_from_spec(SPEC)
sys.modules["prompt_lab"] = prompt_lab
assert SPEC.loader is not None
SPEC.loader.exec_module(prompt_lab)


class PromptLabTest(unittest.TestCase):
    def test_library_contains_core_templates(self):
        library = prompt_lab.PromptLibrary()
        self.assertEqual(["code_explain", "json_extract", "requirements", "summarize"], library.list_templates())

    def test_render_includes_user_input(self):
        rendered = prompt_lab.PromptLibrary().render("summarize", "测试输入")
        self.assertIn("测试输入", rendered)
        self.assertIn("验收标准", rendered)

    def test_empty_input_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "user_input cannot be empty"):
            prompt_lab.PromptLibrary().render("summarize", " ")

    def test_structured_prompt_scores_higher_than_naive_prompt(self):
        checker = prompt_lab.PromptQualityChecker()
        structured = prompt_lab.PromptLibrary().render("requirements", "做一个知识库问答助手")
        naive = prompt_lab.build_naive_prompt("做一个知识库问答助手")
        self.assertGreater(checker.check(structured)["score"], checker.check(naive)["score"])

    def test_mock_runner_returns_stable_json_shape(self):
        output = prompt_lab.MockPromptRunner().run("json_extract", "我想学习 Agent 和 MCP")
        self.assertIn('"keywords"', output)
        self.assertIn('"Agent"', output)


if __name__ == "__main__":
    unittest.main()
