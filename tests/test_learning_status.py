from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "labs" / "learning_status.py"
SPEC = importlib.util.spec_from_file_location("learning_status", MODULE_PATH)
learning_status = importlib.util.module_from_spec(SPEC)
sys.modules["learning_status"] = learning_status
assert SPEC.loader is not None
SPEC.loader.exec_module(learning_status)


class LearningStatusTest(unittest.TestCase):
    def test_discover_stages_in_course_order(self) -> None:
        root = Path(__file__).resolve().parents[1]
        stages = learning_status.discover_stages(root)

        self.assertGreaterEqual(len(stages), 9)
        self.assertEqual("00-ai-foundation", stages[0].slug)
        self.assertEqual("08-eval-security", stages[-1].slug)

    def test_build_report_recommends_first_unfinished_stage(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = learning_status.build_report(root)

        self.assertIn("# AI 学习状态", report)
        self.assertIn("00-ai-foundation", report)
        self.assertIn("推荐下一步", report)
        self.assertIn("lessons/00-ai-foundation/README.md", report)

    def test_progress_file_changes_next_item(self) -> None:
        root = Path(__file__).resolve().parents[1]
        progress = {
            "stages": {
                "00-ai-foundation": {
                    "completed": [
                        "README.md",
                        "01-basic.md",
                        "02-templates.md",
                        "03-exercises.md",
                        "04-exercises-lab/README.md",
                        "05-project.md",
                        "06-project-lab/README.md",
                        "07-review.md",
                    ],
                    "note": "等待自查",
                }
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            progress_path = Path(temp_dir) / "progress.json"
            progress_path.write_text(json.dumps(progress), encoding="utf-8")
            report = learning_status.build_report(root, progress_path, "00-ai-foundation")

        self.assertIn("8/9", report)
        self.assertIn("完成阶段自查：checkpoints/checkpoint-00-ai-foundation.md", report)

    def test_invalid_stage_raises_clear_error(self) -> None:
        root = Path(__file__).resolve().parents[1]

        with self.assertRaisesRegex(ValueError, "未找到阶段"):
            learning_status.build_report(root, stage="99-missing")


if __name__ == "__main__":
    unittest.main()
