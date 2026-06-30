"""最小研究助手：不依赖真实 LLM 的 Agent 教学示例。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


NOTE_DATABASE: dict[str, str] = {
    "agent": "Agent 是围绕目标循环执行的程序：规划、调用工具、观察结果、更新状态。",
    "planner": "Planner 负责把大目标拆成可执行的小步骤，降低一次性完成任务的难度。",
    "tool": "Tool Registry 用来登记可调用工具，让 Agent 通过统一接口使用搜索、读取、写入等能力。",
    "eval": "Eval 用固定样例和评分规则衡量输出质量，帮助发现回归问题。",
    "safety": "安全边界包含权限控制、敏感信息保护、工具调用审计和失败兜底。",
}


@dataclass
class ToolCall:
    """记录一次工具调用，便于课后复盘 Agent 的执行轨迹。"""

    iteration: int
    tool_name: str
    tool_input: str
    observation: str


@dataclass
class ResearchResult:
    """Agent 运行后的完整结果。"""

    topic: str
    plan: list[str]
    tool_log: list[ToolCall]
    report: str
    stopped_by_limit: bool = False


@dataclass
class ToolRegistry:
    """简单工具注册表：把工具名称映射到 Python 函数。"""

    tools: dict[str, Callable[[str], str]] = field(default_factory=dict)

    def register(self, name: str, func: Callable[[str], str]) -> None:
        if not name:
            raise ValueError("工具名称不能为空")
        self.tools[name] = func

    def call(self, name: str, tool_input: str) -> str:
        if name not in self.tools:
            available = ", ".join(sorted(self.tools)) or "无"
            raise KeyError(f"未知工具：{name}。可用工具：{available}")
        return self.tools[name](tool_input)

    def list_tools(self) -> list[str]:
        return sorted(self.tools)


class Planner:
    """规则版 Planner，用关键词生成稳定、可测试的研究计划。"""

    def make_plan(self, topic: str) -> list[str]:
        clean_topic = topic.strip() or "Agent"
        return [
            f"理解主题：{clean_topic}",
            "查找 Agent 基础概念",
            "查找 Planner 的职责",
            "查找 Tool Registry 的作用",
            "查找 Eval 和安全边界",
        ]


class ResearchAgent:
    """最小 Agent：规划，然后在 max_iterations 限制内调用工具并生成报告。"""

    def __init__(self, registry: ToolRegistry, planner: Planner | None = None, max_iterations: int = 4) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations 必须大于 0")
        self.registry = registry
        self.planner = planner or Planner()
        self.max_iterations = max_iterations

    def run(self, topic: str) -> ResearchResult:
        plan = self.planner.make_plan(topic)
        tool_log: list[ToolCall] = []

        for iteration, step in enumerate(plan, start=1):
            if iteration > self.max_iterations:
                break

            tool_name, tool_input = self._choose_tool(step)
            observation = self.registry.call(tool_name, tool_input)
            tool_log.append(
                ToolCall(
                    iteration=iteration,
                    tool_name=tool_name,
                    tool_input=tool_input,
                    observation=observation,
                )
            )

            if "summarize" in self.registry.tools:
                summary = self.registry.call("summarize", observation)
                tool_log.append(
                    ToolCall(
                        iteration=iteration,
                        tool_name="summarize",
                        tool_input=observation,
                        observation=summary,
                    )
                )

        executed_iterations = max((call.iteration for call in tool_log), default=0)
        stopped_by_limit = len(plan) > executed_iterations
        report = build_report(topic=topic, plan=plan, tool_log=tool_log, stopped_by_limit=stopped_by_limit)
        return ResearchResult(topic=topic, plan=plan, tool_log=tool_log, report=report, stopped_by_limit=stopped_by_limit)

    def _choose_tool(self, step: str) -> tuple[str, str]:
        lowered = step.lower()
        if "planner" in lowered:
            return "search_notes", "planner"
        if "tool" in lowered or "registry" in lowered:
            return "search_notes", "tool"
        if "eval" in lowered or "安全" in lowered:
            return "search_notes", "eval"
        return "search_notes", "agent"


def search_notes(keyword: str) -> str:
    """在本地 notes 数据中按关键词查找资料。"""

    key = keyword.strip().lower()
    if key in NOTE_DATABASE:
        return NOTE_DATABASE[key]

    matches = [text for note_key, text in NOTE_DATABASE.items() if key in note_key or key in text.lower()]
    if matches:
        return "\n".join(matches)
    return f"没有找到与 {keyword!r} 完全匹配的笔记，可尝试 agent、planner、tool、eval、safety。"


def summarize_text(text: str) -> str:
    """教学用摘要工具：取第一句话作为摘要。"""

    clean_text = " ".join(text.strip().split())
    if not clean_text:
        return "没有可摘要的内容。"
    for separator in ("。", ".", "！", "?"):
        if separator in clean_text:
            return clean_text.split(separator)[0] + separator
    return clean_text


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("search_notes", search_notes)
    registry.register("summarize", summarize_text)
    return registry


def build_report(topic: str, plan: list[str], tool_log: list[ToolCall], stopped_by_limit: bool) -> str:
    findings = [f"- 第 {call.iteration} 步使用 `{call.tool_name}`：{call.observation}" for call in tool_log]
    sources = sorted({call.tool_input for call in tool_log})

    return "\n".join(
        [
            f"# 研究报告：{topic}",
            "",
            "## 一句话总结",
            "Agent 工程可以从规划、工具调用、日志记录和评测四个角度逐步理解。",
            "",
            "## 研究计划",
            *[f"- {item}" for item in plan],
            "",
            "## 关键发现",
            *(findings or ["- 暂无发现。"]),
            "",
            "## 适合初学者的理解方式",
            "把 Agent 想象成一名实习研究员：先列待办，再查本地资料，每一步都写日志，最后整理报告。",
            "",
            "## 资料来源",
            *[f"- 本地 notes：{source}" for source in sources],
            "",
            "## 运行状态",
            f"- 最大迭代次数：{max((call.iteration for call in tool_log), default=0)} 次已执行",
            f"- 工具调用次数：{len(tool_log)} 次",
            f"- 是否因为 max_iterations 停止：{'是' if stopped_by_limit else '否'}",
            "",
            "## 后续学习建议",
            "- 尝试增加网页搜索工具。",
            "- 尝试把 Planner 替换成真实 LLM。",
            "- 为报告质量增加 Eval。",
            "",
        ]
    )


def save_report(report: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    topic = "Agent 如何完成研究任务"
    agent = ResearchAgent(registry=build_default_registry(), max_iterations=4)
    result = agent.run(topic)
    output_path = Path(__file__).parent / "runs" / "latest-report.md"
    save_report(result.report, output_path)
    print(result.report)
    print(f"报告已保存：{output_path}")


if __name__ == "__main__":
    main()
