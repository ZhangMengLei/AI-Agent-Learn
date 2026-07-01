from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "ui" / "teaching_console.py"
SPEC = importlib.util.spec_from_file_location("teaching_console", MODULE_PATH)
teaching_console = importlib.util.module_from_spec(SPEC)
sys.modules["teaching_console"] = teaching_console
assert SPEC.loader is not None
SPEC.loader.exec_module(teaching_console)


class TeachingConsoleTest(unittest.TestCase):
    def test_build_console_data_contains_teaching_sections(self) -> None:
        data = teaching_console.build_console_data()

        self.assertGreaterEqual(len(data["dashboard"]["stages"]), 9)
        self.assertGreaterEqual(len(data["reader"]["documents"]), 150)
        self.assertTrue(any(document["path"] == "README.md" for document in data["reader"]["documents"]))
        self.assertTrue(any(document["path"] == "labs/roadmap.md" for document in data["reader"]["documents"]))
        self.assertTrue(any(document["path"] == "solutions/README.md" for document in data["reader"]["documents"]))
        self.assertTrue(any(document["path"] == "implementations/README.md" for document in data["reader"]["documents"]))
        self.assertTrue(any(document["path"] == "data/docs/rag-basics.md" for document in data["reader"]["documents"]))
        self.assertTrue(any(collection["slug"] == "solutions" for collection in data["reader"]["collections"]))
        prompt_exercise = next(document for document in data["reader"]["documents"] if document["path"] == "lessons/01-prompt/03-exercises.md")
        prompt_lab = next(document for document in data["reader"]["documents"] if document["path"] == "lessons/01-prompt/04-exercises-lab/README.md")
        prompt_project = next(document for document in data["reader"]["documents"] if document["path"] == "lessons/01-prompt/05-project.md")
        self.assertEqual("solutions/01-prompt/03-exercises.md", prompt_exercise["solution"]["path"])
        self.assertEqual("solutions/01-prompt/04-exercises-lab.md", prompt_lab["solution"]["path"])
        self.assertEqual("solutions/01-prompt/05-project.md", prompt_project["solution"]["path"])
        self.assertIn("content", data["reader"]["documents"][0])
        self.assertGreaterEqual(len(data["prompt"]["templates"]), 4)
        self.assertGreaterEqual(len(data["rag"]["chunks"]), 1)
        self.assertGreaterEqual(len(data["agent"]["toolLog"]), 1)
        self.assertGreaterEqual(data["eval"]["summary"]["total"], 1)

    def test_render_html_embeds_static_app(self) -> None:
        data = teaching_console.build_console_data()
        html = teaching_console.render_html(data)

        self.assertIn("AI-Agent-Learn 本地教学 GUI", html)
        self.assertIn('id="console-data"', html)
        self.assertIn("课程阅读", html)
        self.assertIn("renderReader", html)
        self.assertIn("localStorage", html)
        self.assertIn("导出进度", html)
        self.assertIn("resolveDocumentLink", html)
        self.assertIn("data-doc-link", html)
        self.assertIn("routeForDocument", html)
        self.assertIn("readerSolutionPanel", html)
        self.assertIn("打开答案", html)
        self.assertIn("Prompt Lab", html)
        self.assertIn("RAG 检索", html)
        self.assertIn("Agent Trace", html)
        self.assertIn("Eval 面板", html)
        self.assertNotIn("__CONSOLE_DATA__", html)

    def test_write_console_creates_html_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "console.html"
            saved_path = teaching_console.write_console(output_path)

            self.assertEqual(saved_path, output_path)
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", content)
            self.assertIn("renderDashboard", content)
            self.assertIn("课程阅读器", content)


if __name__ == "__main__":
    unittest.main()
