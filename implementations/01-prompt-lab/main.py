from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    description: str
    role: str
    task: str
    context: str
    constraints: List[str]
    output_format: str
    acceptance_criteria: List[str]

    def render(self, user_input: str) -> str:
        if not user_input.strip():
            raise ValueError("user_input cannot be empty")
        constraints = "\n".join(f"- {item}" for item in self.constraints)
        criteria = "\n".join(f"- {item}" for item in self.acceptance_criteria)
        return f"""角色：{self.role}
任务：{self.task}
上下文：{self.context}

输入：
{user_input}

约束：
{constraints}

输出格式：
{self.output_format}

验收标准：
{criteria}"""


class PromptLibrary:
    def __init__(self) -> None:
        self._templates: Dict[str, PromptTemplate] = {
            "summarize": PromptTemplate(
                name="summarize",
                description="面向初学者的文章总结 Prompt",
                role="中文 AI 学习助手",
                task="总结输入内容，帮助初学者快速理解重点。",
                context="用户正在学习 AI Agent，希望得到准确、简洁、可复盘的总结。",
                constraints=["只基于输入内容回答", "不要补充输入外事实", "用中文回答", "面向初学者"],
                output_format="一句话总结：\n核心要点：\n适合谁看：\n我的建议：",
                acceptance_criteria=["结论不编造", "要点可追溯到输入", "建议具体可执行"],
            ),
            "code_explain": PromptTemplate(
                name="code_explain",
                description="给新手解释代码的 Prompt",
                role="耐心的编程老师",
                task="解释输入代码的整体作用、关键逻辑和易错点。",
                context="读者是能写基础代码但不熟悉该片段的新手。",
                constraints=["先讲整体再讲细节", "避免堆术语", "不要改写原始意图"],
                output_format="整体作用：\n关键逻辑：\n易错点：\n简化版本：",
                acceptance_criteria=["新手能复述代码作用", "指出至少一个易错点", "简化版本保留核心逻辑"],
            ),
            "requirements": PromptTemplate(
                name="requirements",
                description="需求拆解 Prompt",
                role="经验丰富的产品型工程师",
                task="把用户需求拆解成目标、用户、功能、边界和验收标准。",
                context="用于把模糊想法变成可执行的小项目说明。",
                constraints=["不要扩大需求范围", "明确不做什么", "优先给最小可行版本"],
                output_format="目标：\n用户：\n核心功能：\n不做范围：\n验收标准：",
                acceptance_criteria=["能指导下一步实现", "边界清晰", "验收标准可检查"],
            ),
            "json_extract": PromptTemplate(
                name="json_extract",
                description="严格 JSON 信息抽取 Prompt",
                role="结构化信息抽取器",
                task="从输入中抽取 name、job、goal、keywords 字段。",
                context="输出会被程序解析，所以必须是合法 JSON。",
                constraints=["只输出 JSON", "缺失字段用 null", "keywords 必须是数组", "不要输出 Markdown"],
                output_format='{"name": string|null, "job": string|null, "goal": string|null, "keywords": string[]}',
                acceptance_criteria=["JSON 可解析", "字段完整", "不猜测缺失信息"],
            ),
        }

    def list_templates(self) -> List[str]:
        return sorted(self._templates)

    def get_template(self, name: str) -> PromptTemplate:
        try:
            return self._templates[name]
        except KeyError as exc:
            raise KeyError(f"unknown template: {name}") from exc

    def render(self, name: str, user_input: str) -> str:
        return self.get_template(name).render(user_input)


class PromptQualityChecker:
    markers = {
        "role": "角色：",
        "task": "任务：",
        "context": "上下文：",
        "constraints": "约束：",
        "output_format": "输出格式：",
        "acceptance_criteria": "验收标准：",
    }

    def check(self, prompt: str) -> Dict[str, object]:
        passed = [name for name, marker in self.markers.items() if marker in prompt]
        missing = [name for name in self.markers if name not in passed]
        score = round(len(passed) / len(self.markers) * 100)
        suggestions = [f"补充 {name}" for name in missing]
        return {"score": score, "passed": passed, "missing": missing, "suggestions": suggestions}


class MockPromptRunner:
    def run(self, template_name: str, user_input: str) -> str:
        text = user_input.strip()
        if template_name == "json_extract":
            keywords = [word for word in ["AI", "Agent", "Prompt", "MCP"] if word.lower() in text.lower()]
            return '{"name": null, "job": null, "goal": "学习或整理输入信息", "keywords": ' + str(keywords).replace("'", '"') + "}"
        if template_name == "code_explain":
            return "整体作用：这段代码完成一个小任务。\n关键逻辑：读取输入，处理数据，输出结果。\n易错点：忽略边界输入。\n简化版本：输入 -> 处理 -> 输出。"
        if template_name == "requirements":
            return "目标：完成一个最小可运行版本。\n用户：学习者或开发者。\n核心功能：输入需求并拆解任务。\n不做范围：不接生产系统。\n验收标准：能按清单检查。"
        return "一句话总结：输入内容介绍了一个核心概念。\n核心要点：\n- 主题明确\n- 适合入门\n适合谁看：初学者。\n我的建议：先复述概念，再做小练习。"


def build_naive_prompt(user_input: str) -> str:
    return f"帮我处理一下：{user_input}"


def run_demo(template_name: str, user_input: str, compare: bool) -> str:
    library = PromptLibrary()
    checker = PromptQualityChecker()
    runner = MockPromptRunner()
    structured = library.render(template_name, user_input)
    structured_score = checker.check(structured)
    lines = [f"模板：{template_name}", "", "结构化 Prompt：", structured, "", f"质量得分：{structured_score['score']}"]
    if structured_score["suggestions"]:
        lines.append("改进建议：" + "；".join(structured_score["suggestions"]))
    lines.extend(["", "Mock 输出：", runner.run(template_name, user_input)])
    if compare:
        naive = build_naive_prompt(user_input)
        naive_score = checker.check(naive)
        lines.extend(["", "对比：", f"随口 Prompt 得分：{naive_score['score']}", f"结构化 Prompt 得分：{structured_score['score']}"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt 模板与质量检查教学 Demo")
    parser.add_argument("--template", default="summarize", choices=PromptLibrary().list_templates())
    parser.add_argument("--input", default="Prompt 是人与大模型协作时的任务说明书。")
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()
    print(run_demo(args.template, args.input, args.compare))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
