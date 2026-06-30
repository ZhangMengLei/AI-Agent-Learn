"""研究助手 Agent 的单元测试。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "implementations" / "05-research-agent" / "research_agent.py"
SPEC = importlib.util.spec_from_file_location("research_agent", MODULE_PATH)
research_agent = importlib.util.module_from_spec(SPEC)
sys.modules["research_agent"] = research_agent
assert SPEC.loader is not None
SPEC.loader.exec_module(research_agent)


class ResearchAgentTest(unittest.TestCase):
    def test_agent_calls_tools_and_generates_report(self) -> None:
        registry = research_agent.build_default_registry()
        agent = research_agent.ResearchAgent(registry=registry, max_iterations=3)

        result = agent.run("Agent 入门")

        self.assertEqual(len(result.tool_log), 6)
        self.assertEqual({call.iteration for call in result.tool_log}, {1, 2, 3})
        self.assertTrue(result.stopped_by_limit)
        self.assertIn("# 研究报告：Agent 入门", result.report)
        self.assertIn("Tool Registry", result.report)
        self.assertIn("summarize", result.report)
        self.assertIn("是否因为 max_iterations 停止：是", result.report)

    def test_tool_registry_rejects_unknown_tool(self) -> None:
        registry = research_agent.ToolRegistry()

        with self.assertRaises(KeyError):
            registry.call("missing", "agent")

    def test_search_notes_uses_local_data(self) -> None:
        observation = research_agent.search_notes("planner")

        self.assertIn("Planner", observation)
        self.assertIn("拆", observation)


if __name__ == "__main__":
    unittest.main()
