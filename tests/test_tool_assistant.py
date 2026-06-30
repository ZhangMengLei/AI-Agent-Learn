import importlib.util
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = PROJECT_ROOT / "implementations" / "03-tool-assistant" / "main.py"

spec = importlib.util.spec_from_file_location("tool_assistant_main", MAIN_PATH)
tool_assistant = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = tool_assistant
spec.loader.exec_module(tool_assistant)


class ToolAssistantTests(unittest.TestCase):
    def test_model_selects_weather_tool(self):
        model = tool_assistant.MockModel()

        call = model.plan("北京天气怎么样")

        self.assertIsNotNone(call)
        self.assertEqual(call.name, "mock_weather")
        self.assertEqual(call.arguments, {"city": "北京"})

    def test_calculator_executes_expression(self):
        registry = tool_assistant.build_default_registry()
        call = tool_assistant.ToolCall("calculator", {"expression": "1 + 2 * 3"})

        result = registry.execute(call)

        self.assertTrue(result.ok)
        self.assertEqual(result.content, "1 + 2 * 3 = 7")
        self.assertEqual(registry.log[-1].status, "success")

    def test_write_permission_can_be_denied_and_allowed(self):
        registry = tool_assistant.build_default_registry()
        call = tool_assistant.ToolCall("mock_notes", {"text": "学习 Tool Use"})

        denied = registry.execute(call, confirm_permission=lambda spec, args: False)
        allowed = registry.execute(call, confirm_permission=lambda spec, args: True)

        self.assertFalse(denied.ok)
        self.assertIn("Permission denied", denied.error)
        self.assertTrue(allowed.ok)
        self.assertIn("已记录笔记", allowed.content)
        self.assertEqual(registry.log[-2].status, "denied")
        self.assertEqual(registry.log[-1].status, "success")

    def test_unknown_tool_returns_error_and_logs(self):
        registry = tool_assistant.build_default_registry()
        call = tool_assistant.ToolCall("not_exists", {})

        result = registry.execute(call)

        self.assertFalse(result.ok)
        self.assertEqual(result.error, "Unknown tool: not_exists")
        self.assertEqual(registry.log[-1].tool_name, "not_exists")
        self.assertEqual(registry.log[-1].status, "error")

    def test_argument_validation_rejects_wrong_type(self):
        registry = tool_assistant.build_default_registry()
        call = tool_assistant.ToolCall("mock_weather", {"city": 123})

        result = registry.execute(call)

        self.assertFalse(result.ok)
        self.assertIn("Invalid type for city", result.error)


if __name__ == "__main__":
    unittest.main()
