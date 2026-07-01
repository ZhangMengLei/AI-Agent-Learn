"""学习状态导航工具。

这个脚本只读取本地课程目录和可选的进度 JSON，不调用任何外部模型服务。
它的目标是帮助学习者回答三个问题：

1. 当前课程有哪些阶段？
2. 我已经完成了哪些材料？
3. 下一步最小行动是什么？
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_LESSON_FILES = (
    "README.md",
    "01-basic.md",
    "02-templates.md",
    "03-exercises.md",
    "04-exercises-lab/README.md",
    "05-project.md",
    "06-project-lab/README.md",
    "07-review.md",
)

DEMO_COMMANDS = {
    "01-prompt": "make demo-prompt",
    "02-llm-api": "make demo-llm",
    "03-tool-use": "make demo-tool",
    "04-rag": 'make demo-rag QUERY="Agent 和 Chatbot 区别是什么"',
    "05-agent": "make demo-agent",
    "06-mcp": "make demo-mcp",
    "07-claude-code": "make demo-claude-code",
    "08-eval-security": "make demo-eval",
}


@dataclass(frozen=True)
class Stage:
    slug: str
    title: str
    lesson_dir: Path
    checkpoint_path: Path


@dataclass(frozen=True)
class StageStatus:
    stage: Stage
    completed_items: tuple[str, ...]
    required_items: tuple[str, ...]
    note: str

    @property
    def completed_count(self) -> int:
        return len(set(self.completed_items) & set(self.required_items))

    @property
    def total_count(self) -> int:
        return len(self.required_items)

    @property
    def percent(self) -> int:
        if self.total_count == 0:
            return 0
        return round(self.completed_count / self.total_count * 100)

    @property
    def is_complete(self) -> bool:
        return self.completed_count == self.total_count

    @property
    def next_item(self) -> str:
        completed = set(self.completed_items)
        for item in self.required_items:
            if item not in completed:
                return item
        return "阶段复盘"


def project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_stages(root: Path) -> list[Stage]:
    lessons_dir = root / "lessons"
    stages: list[Stage] = []
    for lesson_dir in sorted(path for path in lessons_dir.iterdir() if path.is_dir()):
        readme = lesson_dir / "README.md"
        if not readme.exists():
            continue
        title = extract_title(readme) or lesson_dir.name
        stage_id = lesson_dir.name.split("-", 1)[0]
        stages.append(
            Stage(
                slug=lesson_dir.name,
                title=title,
                lesson_dir=lesson_dir,
                checkpoint_path=root / "checkpoints" / f"checkpoint-{stage_id}-{lesson_dir.name.split('-', 1)[1]}.md",
            )
        )
    return stages


def extract_title(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return None


def load_progress(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"stages": {}}
    if not path.exists():
        raise FileNotFoundError(f"未找到进度文件：{path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("进度文件顶层必须是 JSON object")
    stages = data.setdefault("stages", {})
    if not isinstance(stages, dict):
        raise ValueError("progress.stages 必须是 object")
    return data


def required_items_for(stage: Stage) -> tuple[str, ...]:
    existing_items = tuple(item for item in REQUIRED_LESSON_FILES if (stage.lesson_dir / item).exists())
    if stage.checkpoint_path.exists():
        return (*existing_items, "checkpoint")
    return existing_items


def stage_status(stage: Stage, progress: dict[str, Any]) -> StageStatus:
    stage_progress = progress.get("stages", {}).get(stage.slug, {})
    if not isinstance(stage_progress, dict):
        raise ValueError(f"{stage.slug} 的进度记录必须是 object")

    completed = stage_progress.get("completed", [])
    if not isinstance(completed, list) or not all(isinstance(item, str) for item in completed):
        raise ValueError(f"{stage.slug}.completed 必须是字符串数组")

    note = stage_progress.get("note", "")
    if not isinstance(note, str):
        raise ValueError(f"{stage.slug}.note 必须是字符串")

    return StageStatus(
        stage=stage,
        completed_items=tuple(completed),
        required_items=required_items_for(stage),
        note=note,
    )


def summarize_statuses(stages: list[Stage], progress: dict[str, Any]) -> list[StageStatus]:
    return [stage_status(stage, progress) for stage in stages]


def choose_next_status(statuses: list[StageStatus], preferred_stage: str | None = None) -> StageStatus | None:
    if preferred_stage:
        for status in statuses:
            if status.stage.slug == preferred_stage:
                return status
        raise ValueError(f"未找到阶段：{preferred_stage}")

    for status in statuses:
        if not status.is_complete:
            return status
    return statuses[-1] if statuses else None


def next_actions(status: StageStatus) -> list[str]:
    slug = status.stage.slug
    lesson_ref = f"lessons/{slug}/{status.next_item}"
    actions = [f"阅读或完成：{lesson_ref}"]

    if status.next_item == "checkpoint":
        checkpoint_ref = status.stage.checkpoint_path.relative_to(status.stage.lesson_dir.parents[1])
        actions[0] = f"完成阶段自查：{checkpoint_ref}"

    demo_command = DEMO_COMMANDS.get(slug)
    if demo_command:
        actions.append(f"运行配套 demo：{demo_command}")

    actions.append("记录 1 个卡点、1 个已经理解的概念、1 个下一步实验。")
    return actions


def render_report(statuses: list[StageStatus], next_status: StageStatus | None) -> str:
    lines = ["# AI 学习状态", ""]
    lines.append("| 阶段 | 主题 | 完成度 | 下一项 | 备注 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for status in statuses:
        note = status.note or "-"
        lines.append(
            f"| {status.stage.slug} | {status.stage.title} | "
            f"{status.completed_count}/{status.total_count} ({status.percent}%) | "
            f"{status.next_item} | {note} |"
        )

    if next_status is not None:
        lines.extend(["", "## 推荐下一步", ""])
        for index, action in enumerate(next_actions(next_status), start=1):
            lines.append(f"{index}. {action}")

    lines.extend(
        [
            "",
            "提示：可以复制 `data/notes/learning-progress.example.json` 为自己的进度文件，",
            "然后运行 `make learn-status PROGRESS=你的进度文件.json`。",
        ]
    )
    return "\n".join(lines)


def build_report(root: Path, progress_path: Path | None = None, stage: str | None = None) -> str:
    stages = discover_stages(root)
    progress = load_progress(progress_path)
    statuses = summarize_statuses(stages, progress)
    next_status = choose_next_status(statuses, stage)
    return render_report(statuses, next_status)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查看 AI-Agent-Learn 的学习状态和推荐下一步。")
    parser.add_argument("--progress", type=Path, help="可选的学习进度 JSON 文件。")
    parser.add_argument("--stage", help="只为指定阶段生成下一步建议，例如 04-rag。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(build_report(project_root_from_script(), args.progress, args.stage))


if __name__ == "__main__":
    main()
